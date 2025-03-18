/**
 * @file ball_query.cpp
 *
 * Copyright (C) 2024. Huawei Technologies Co., Ltd. All rights reserved.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 */
#include "kernel_operator.h"
#define DIVUP(m, n) ((m) / (n) + ((m) % (n) > 0))

constexpr int32_t USE_CORE_NUM = 8; // num of core used

class KernalBallquery {
public:
  __aicore__ inline KernalBallquery() {}
  __aicore__ inline void Init(int32_t n, int32_t m, int32_t nsample,
                              GM_ADDR newXyz, GM_ADDR xyz, GM_ADDR idx) {
    int32_t TOTAL_LENGTH = m;
    int32_t BLOCK_LENGTH = TOTAL_LENGTH / USE_CORE_NUM;
    newXyzGm.SetGlobalBuffer((__gm__ int32_t *)newXyz +
                                 BLOCK_LENGTH * AscendC::GetBlockIdx() * 3,
                             BLOCK_LENGTH * 3);
    xyzGm.SetGlobalBuffer((__gm__ int32_t *)xyz, n * 3);
    idxGm.SetGlobalBuffer((__gm__ int32_t *)idx +
                              BLOCK_LENGTH * AscendC::GetBlockIdx() * nsample,
                          BLOCK_LENGTH * nsample);
    pipe.InitBuffer(inQueueNewxyz, 1, 3 * sizeof(int32_t));
    pipe.InitBuffer(inQueueXyz, 1, n * 3 * sizeof(int32_t));
    pipe.InitBuffer(outQueueIdx, 1, nsample * sizeof(int32_t));
  }
  __aicore__ inline void Process(int32_t n, int32_t m, int32_t min_radius,
                                 int32_t max_radius, int32_t nsample) {
    int32_t loopCount = m / USE_CORE_NUM;
    for (int32_t i = 0; i < loopCount; i++) {
      CopyIn(i, n);
      Compute(i, n, min_radius, max_radius, nsample);
      CopyOut(i, nsample);
    }
  }

private:
  __aicore__ inline void CopyIn(int32_t progress, int n) {
    AscendC::LocalTensor<int32_t> newXyzLocal =
        inQueueNewxyz.AllocTensor<int32_t>();
    AscendC::LocalTensor<int32_t> xyzLocal = inQueueXyz.AllocTensor<int32_t>();
    AscendC::DataCopy(newXyzLocal, newXyzGm[progress * 3], 8);
    AscendC::DataCopy(xyzLocal, xyzGm, n * 3);
    inQueueNewxyz.EnQue(newXyzLocal);
    inQueueXyz.EnQue(xyzLocal);
  }
  __aicore__ inline void Compute(int32_t progress, int32_t n,
                                 int32_t min_radius, int32_t max_radius,
                                 int32_t nsample) {
    AscendC::LocalTensor<int32_t> newXyz = inQueueNewxyz.DeQue<int32_t>();
    AscendC::LocalTensor<int32_t> xyz = inQueueXyz.DeQue<int32_t>();
    AscendC::LocalTensor<int32_t> idx = outQueueIdx.AllocTensor<int32_t>();
    int32_t max_radius2 = max_radius * max_radius;
    int32_t min_radius2 = min_radius * min_radius;
    int32_t new_x = newXyz.GetValue(0);
    int32_t new_y = newXyz.GetValue(1);
    int32_t new_z = newXyz.GetValue(2);

    int cnt = 0;
    for (int k = 0; k < n; ++k) {
      int32_t x = xyz.GetValue(k * 3 + 0);
      int32_t y = xyz.GetValue(k * 3 + 1);
      int32_t z = xyz.GetValue(k * 3 + 2);
      int32_t d2 = (new_x - x) * (new_x - x) + (new_y - y) * (new_y - y) +
                   (new_z - z) * (new_z - z);
      if (d2 == 0 || (d2 >= min_radius2 && d2 < max_radius2)) {
        if (cnt == 0) {
          for (int l = 0; l < nsample; ++l) {
            idx.SetValue(l, k);
          }
        }
        idx.SetValue(cnt, k);
        ++cnt;
        if (cnt >= nsample)
          break;
      }
    }
    outQueueIdx.EnQue<int32_t>(idx);
    inQueueNewxyz.FreeTensor(newXyz);
    inQueueXyz.FreeTensor(xyz);
  }
  __aicore__ inline void CopyOut(int32_t progress, int32_t nsample) {
    AscendC::LocalTensor<int32_t> idx = outQueueIdx.DeQue<int32_t>();
    AscendC::DataCopy(idxGm[progress * nsample], idx, nsample);
    outQueueIdx.FreeTensor(idx);
  }

private:
  AscendC::TPipe pipe;
  AscendC::TQue<AscendC::QuePosition::VECIN, 1> inQueueNewxyz, inQueueXyz;
  AscendC::TQue<AscendC::QuePosition::VECOUT, 1> outQueueIdx;
  AscendC::GlobalTensor<int32_t> newXyzGm;
  AscendC::GlobalTensor<int32_t> xyzGm;
  AscendC::GlobalTensor<int32_t> idxGm;
};

extern "C" __global__ __aicore__ void
ball_query_kernel(int32_t n, int32_t m, int32_t min_radius, int32_t max_radius,
                  int32_t nsample, GM_ADDR new_xyz, GM_ADDR xyz, GM_ADDR idx) {
  KernalBallquery op;
  op.Init(n, m, nsample, new_xyz, xyz, idx);
  op.Process(n, m, min_radius, max_radius, nsample);
}

#ifndef ASCENDC_CPU_DEBUG
void ball_query_do(void *stream, uint8_t *x, uint8_t *y, uint8_t *z, int32_t n,
                   int32_t m, int32_t min_radius, int32_t max_radius,
                   int32_t nsample) {
  ball_query_kernel<<<blockDim, nullptr, stream>>>(n, m, min_radius,
                                                   max_radius.nsample, x, y, z);
}
#endif
