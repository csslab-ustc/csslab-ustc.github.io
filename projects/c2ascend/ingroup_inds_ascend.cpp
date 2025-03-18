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

constexpr int32_t TOTAL_LENGTH = 32; // total length of data
constexpr int32_t USE_CORE_NUM = 1;  // num of core used
constexpr int32_t BLOCK_LENGTH =
    TOTAL_LENGTH / USE_CORE_NUM;  // length computed of each core
constexpr int32_t TILE_NUM = 1;   // split data into 8 tiles for each core
constexpr int32_t BUFFER_NUM = 1; // tensor num for each queue
constexpr int32_t TILE_LENGTH =
    BLOCK_LENGTH / TILE_NUM /
    BUFFER_NUM; // separate to 2 parts, due to double buffer

class KernelIngroupIndex {
public:
  __aicore__ inline KernelIngroupIndex() {}
  __aicore__ inline void Init(GM_ADDR group_inds, GM_ADDR out_inds,
                              GM_ADDR ingroup_counter, int32_t N,
                              int32_t max_group_id) {
    group_indsGm.SetGlobalBuffer((__gm__ uint32_t *)group_inds, BLOCK_LENGTH);
    out_indsGm.SetGlobalBuffer((__gm__ uint32_t *)out_inds, BLOCK_LENGTH);
    ingroup_counterGm.SetGlobalBuffer((__gm__ uint32_t *)ingroup_counter,
                                      max_group_id);
    pipe.InitBuffer(inQueue_group_inds, BUFFER_NUM,
                    TILE_LENGTH * sizeof(uint32_t));
    pipe.InitBuffer(inQueue_ingroup_counter, BUFFER_NUM,
                    max_group_id * sizeof(uint32_t));
    pipe.InitBuffer(outQueue_out_inds, BUFFER_NUM,
                    TILE_LENGTH * sizeof(uint32_t));
    pipe.InitBuffer(outQueue_ingroup_counter, BUFFER_NUM,
                    max_group_id * sizeof(uint32_t));
  }
  __aicore__ inline void Process() {
    int32_t loopCount = TILE_NUM * BUFFER_NUM;
    for (int32_t i = 0; i < loopCount; i++) {
      CopyIn(i);
      Compute(i);
      CopyOut(i);
    }
  }

private:
  __aicore__ inline void CopyIn(int32_t progress) {
    AscendC::LocalTensor<uint32_t> group_indsLocal =
        inQueue_group_inds.AllocTensor<uint32_t>();
    AscendC::LocalTensor<uint32_t> ingroup_counterLocal =
        inQueue_ingroup_counter.AllocTensor<uint32_t>();
    AscendC::DataCopy(group_indsLocal, group_indsGm[progress * TILE_LENGTH],
                      TILE_LENGTH);
    AscendC::DataCopy(ingroup_counterLocal, ingroup_counterGm, max_group_id);
    inQueue_group_inds.EnQue(group_indsLocal);
    inQueue_ingroup_counter.EnQue(ingroup_counterLocal);
  }
  __aicore__ inline void Compute(int32_t progress) {
    AscendC::LocalTensor<uint32_t> group_indsLocal =
        inQueue_group_inds.DeQue<uint32_t>();
    AscendC::LocalTensor<uint32_t> ingroup_counterLocal =
        inQueue_ingroup_counter.DeQue<uint32_t>();
    AscendC::LocalTensor<uint32_t> out_indsLocal =
        outQueue_out_inds.AllocTensor<uint32_t>();
    AscendC::LocalTensor<uint32_t> ingroup_counter_outLocal =
        outQueue_ingroup_counter.AllocTensor<uint32_t>();

    for (uint32_t i = 0; i < TILE_LENGTH; i++) {
      uint32_t this_group_id = group_indsLocal.GetValue(i);
      uint32_t cnt = ingroup_counterLocal.GetValue(this_group_id);
      uint32_t cnt_new = cnt + 1;
      ingroup_counterLocal.SetValue(this_group_id, cnt_new);
      out_indsLocal.SetValue(i, cnt_new);
    }

    AscendC::DataCopy(ingroup_counter_outLocal, ingroup_counterLocal,
                      max_group_id);
    outQueue_out_inds.EnQue<uint32_t>(out_indsLocal);
    outQueue_ingroup_counter.EnQue<uint32_t>(ingroup_counter_outLocal);
    inQueue_group_inds.FreeTensor(group_indsLocal);
    inQueue_ingroup_counter.FreeTensor(ingroup_counterLocal);
  }
  __aicore__ inline void CopyOut(int32_t progress) {
    AscendC::LocalTensor<uint32_t> out_indsLocal =
        outQueue_out_inds.DeQue<uint32_t>();
    AscendC::LocalTensor<uint32_t> ingroup_counter_outLocal =
        outQueue_ingroup_counter.DeQue<uint32_t>();
    AscendC::DataCopy(out_indsGm, out_indsLocal, TILE_LENGTH);
    AscendC::DataCopy(ingroup_counterGm, ingroup_counter_outLocal,
                      max_group_id);
    outQueue_out_inds.FreeTensor(out_indsLocal);
    outQueue_ingroup_counter.FreeTensor(ingroup_counter_outLocal);
  }

private:
  AscendC::TPipe pipe;
  AscendC::TQue<AscendC::QuePosition::VECIN, BUFFER_NUM> inQueue_group_inds,
      inQueue_ingroup_counter;
  AscendC::TQue<AscendC::QuePosition::VECOUT, BUFFER_NUM> outQueue_out_inds,
      outQueue_ingroup_counter;
  AscendC::GlobalTensor<uint32_t> group_indsGm;
  AscendC::GlobalTensor<uint32_t> ingroup_counterGm;
  AscendC::GlobalTensor<uint32_t> out_indsGm;
  int32_t max_group_id = 16;
};

extern "C" __global__ __aicore__ void
ingroup_inds_kernel(GM_ADDR group_inds, GM_ADDR out_inds,
                    GM_ADDR ingroup_counter, int32_t N, int32_t max_group_id) {
  KernelAdd op;
  op.Init(group_inds, out_inds, ingroup_counter, N, max_group_id);
  op.Process();
}

#ifndef ASCENDC_CPU_DEBUG
void ingroup_index_do(uint32_t blockDim, void *stream, uint8_t *group_inds,
                      uint8_t *out_inds, uint8_t *ingroup_counter, int32_t N,
                      int32_t max_group_id) {
  ingroup_inds_kernel<<<blockDim, nullptr, stream>>>(
      group_inds, out_inds, ingroup_counter, N, max_group_id);
}
#endif
