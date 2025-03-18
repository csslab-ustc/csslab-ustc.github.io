/**
 * @file add_custom.cpp
 *
 * Copyright (C) 2024. Huawei Technologies Co., Ltd. All rights reserved.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 */
#include "kernel_operator.h"

class KernelGatherPoints {
public:
  __aicore__ inline KernelGatherPoints() {}
  __aicore__ inline void Init(int32_t b, int32_t c, int32_t n, int32_t m,
                              uint32_t *points, uint32_t *idx, uint32_t *out) {
    pointsGm.SetGlobalBuffer((__gm__ int32_t *)points, b * c * n);
    idxGm.SetGlobalBuffer((__gm__ int32_t *)idx, b * m);
    outGm.SetGlobalBuffer((__gm__ int32_t *)out, b * c * m);
    pipe.InitBuffer(inQueuePoints, 1, b * c * n * sizeof(int32_t));
    pipe.InitBuffer(inQueueIdx, 1, b * m * sizeof(int32_t));
    pipe.InitBuffer(outQueueOut, 1, b * c * m * sizeof(int32_t));
  }
  __aicore__ inline void Process(int32_t b, int32_t c, int32_t n, int32_t m) {
    int32_t loopCount = b * c * m;
    for (int32_t i = 0; i < loopCount; i++) {
      CopyIn(i, b, c, n, m);
      Compute(i, b, c, n, m);
      CopyOut(i, b, c, n, m);
    }
  }

private:
  __aicore__ inline void CopyIn(int32_t progress, int32_t b, int32_t c,
                                int32_t n, int32_t m) {
    AscendC::LocalTensor<int32_t> pointsLocal =
        inQueuePoints.AllocTensor<int32_t>();
    AscendC::LocalTensor<int32_t> idxLocal = inQueueIdx.AllocTensor<int32_t>();
    AscendC::DataCopy(pointsLocal, pointsGm, b * c * n);
    AscendC::DataCopy(idxLocal, idxGm, b * m);
    inQueuePoints.EnQue(pointsLocal);
    inQueueIdx.EnQue(idxLocal);
  }
  __aicore__ inline void Compute(int32_t progress, int32_t b, int32_t c,
                                 int32_t n, int32_t m) {
    AscendC::LocalTensor<int32_t> pointsLocal = inQueuePoints.DeQue<int32_t>();
    AscendC::LocalTensor<int32_t> idxLocal = inQueueIdx.DeQue<int32_t>();
    AscendC::LocalTensor<int32_t> outLocal = outQueueOut.AllocTensor<int32_t>();
    int32_t b_idx = progress / (m * c);
    int32_t c_idx = (progress / m) % c;
    int32_t m_idx = progress % m;
    int32_t index = idxLocal.GetValue(b_idx * m + m_idx);
    int32_t value = pointsLocal.GetValue(b_idx * (c * n) + c_idx * n + index);
    outLocal.SetValue(progress, value);
    outQueueOut.EnQue<int32_t>(outLocal);
    inQueuePoints.FreeTensor(pointsLocal);
    inQueueIdx.FreeTensor(idxLocal);
  }
  __aicore__ inline void CopyOut(int32_t progress, int32_t b, int32_t c,
                                 int32_t n, int32_t m) {
    AscendC::LocalTensor<int32_t> outLocal = outQueueOut.DeQue<int32_t>();
    AscendC::DataCopy(outGm, outLocal, b * c * m);
    outQueueOut.FreeTensor(outLocal);
  }

private:
  AscendC::TPipe pipe;
  AscendC::TQue<AscendC::QuePosition::VECIN, 1> inQueuePoints, inQueueIdx;
  AscendC::TQue<AscendC::QuePosition::VECOUT, 1> outQueueOut;
  AscendC::GlobalTensor<int32_t> pointsGm;
  AscendC::GlobalTensor<int32_t> idxGm;
  AscendC::GlobalTensor<int32_t> outGm;
};

extern "C" __global__ __aicore__ void
gather_points_kernel(int32_t b, int32_t c, int32_t n, int32_t m,
                     uint32_t *points, uint32_t *idx, uint32_t *out) {
  KernelGatherPoints op;
  op.Init(b, c, n, m, points, idx, out);
  op.Process(b, c, n, m);
}

#ifndef ASCENDC_CPU_DEBUG
void gather_points_do(uint32_t blockDim, void *stream, int32_t b, int32_t c,
                      int32_t n, int32_t m, int32_t *points, int32_t *idx,
                      int32_t *out) {
  gather_points_kernel<<<blockDim, nullptr, stream>>>(b, c, n, m, points, idx,
                                                      out);
}
#endif
