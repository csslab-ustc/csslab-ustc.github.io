/**
 * @file gather_points.cpp
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
                              GM_ADDR points, GM_ADDR idx, GM_ADDR out) {
    // int32_t BLOCK_LENGTH = c * n;
    // int32_t IDX_BLOCK_LENGTH = m;
    // int32_t OUT_BLOCK_LENGTH = c * m;
    pointsGm.SetGlobalBuffer((__gm__ half *)points, b * c * n);
    idxGm.SetGlobalBuffer((__gm__ half *)idx, b * m);
    outGm.SetGlobalBuffer((__gm__ half *)out, b * c * m);
    pipe.InitBuffer(inQueuePoints, 1, b * c * n * sizeof(half));
    pipe.InitBuffer(inQueueIdx, 1, b * m * sizeof(half));
    pipe.InitBuffer(outQueueOut, 1, b * c * m * sizeof(half));
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
    AscendC::LocalTensor<half> pointsLocal = inQueuePoints.AllocTensor<half>();
    AscendC::LocalTensor<half> idxLocal = inQueueIdx.AllocTensor<half>();
    AscendC::DataCopy(pointsLocal, pointsGm, b * c * n);
    AscendC::DataCopy(idxLocal, idxGm, b * m);
    inQueuePoints.EnQue(pointsLocal);
    inQueueIdx.EnQue(idxLocal);
  }

  __aicore__ inline void Compute(int32_t progress, int32_t b, int32_t c,
                                 int32_t n, int32_t m) {
    AscendC::LocalTensor<half> pointsLocal = inQueuePoints.DeQue<half>();
    AscendC::LocalTensor<half> idxLocal = inQueueIdx.DeQue<half>();
    AscendC::LocalTensor<half> outLocal = outQueueOut.AllocTensor<half>();
    int32_t b_idx = progress / (m * c);
    int32_t c_idx = (progress / m) % c;
    int32_t m_idx = progress % m;
    // outLocal[progress] = pointsLocal[b_idx * (c * n) + c_idx * n +
    // idxLocal[b_idx * m + m_idx]];
    outLocal.SetValue(pointsLocal.GetValue(
        b_idx * (c * n) + c_idx * n + idxLocal.GetValue(b_idx * m + m_idx)));
    outQueueZ.EnQue<half>(outLocal);
    inQueueX.FreeTensor(pointsLocal);
    inQueueY.FreeTensor(idxLocal);
  }

  __aicore__ inline void CopyOut(int32_t progress, int32_t b, int32_t c,
                                 int32_t n, int32_t m) {
    AscendC::LocalTensor<half> outLocal = outQueueOut.DeQue<half>();
    AscendC::DataCopy(outGm, outLocal, b * c * m);
    outQueueZ.FreeTensor(outLocal);
  }

private:
  AscendC::TPipe pipe;
  AscendC::TQue<AscendC::QuePosition::VECIN, 1> inQueuePoints, inQueueIdx;
  AscendC::TQue<AscendC::QuePosition::VECOUT, 1> outQueueOut;
  AscendC::GlobalTensor<half> pointsGm;
  AscendC::GlobalTensor<half> idxGm;
  AscendC::GlobalTensor<half> outGm;
};

extern "C" __global__ __aicore__ void
gather_points_kernel(int32_t b, int32_t c, int32_t n, int32_t m, GM_ADDR points,
                     GM_ADDR idx, GM_ADDR out) {
  KernelGatherPoints op;
  op.Init(b, c, n, m, points, idx, out);
  op.Process(b, c, n, m);
}

#ifndef ASCENDC_CPU_DEBUG
void gather_points_do(uint32_t blockDim, void *stream, int32_t b, int32_t c,
                      int32_t n, int32_t m, uint8_t *points, uint8_t *idx,
                      uint8_t *out) {
  gather_points_kernel<<<1, nullptr, stream>>>(b, c, n, m, points, idx, out);
}
#endif
