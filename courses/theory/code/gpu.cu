#include <stdio.h>
#include <math.h>

extern "C"{

struct point_t{
    float x;
    float y;
};

__global__ void line_kernel(struct point_t *pt,
    int *ret_values,
    int size){
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    if(tid < size){
        float x = (pt + tid)->x;
        float y = (pt + tid)->y;
        ret_values[tid] = (fabs(2 * x + 3 - y) <= 1e-2);
    }
}

__global__ void circle_kernel(struct point_t *pt,
    int *ret_values,
    int size){
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    if(tid < size){
        float x = (pt + tid)->x;
        float y = (pt + tid)->y;
        ret_values[tid] = (fabs(x * x + y*y - 5) <= 1e-2);
    }
}

__global__ void ellipse_kernel(struct point_t *pt,
    int *ret_values,
    int size){
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    if(tid < size){
        float x = (pt + tid)->x;
        float y = (pt + tid)->y;
        ret_values[tid] = (fabs(x * x/4 + y*y/2 - 5) <= 1e-2);
    }
}

__global__ void parabola_kernel(struct point_t *pt,
    int *ret_values,
    int size){
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    if(tid < size){
        float x = (pt + tid)->x;
        float y = (pt + tid)->y;
        ret_values[tid] = (fabs(x * 4 - y*y) <= 1e-2);
    }
}

__global__ void hyperbola_kernel(struct point_t *pt,
    int *ret_values,
    int size){
    int tid = blockDim.x * blockIdx.x + threadIdx.x;
    if(tid < size){
        float x = (pt + tid)->x;
        float y = (pt + tid)->y;
        ret_values[tid] = (fabs(x * x/4 + y*y/2 - 1) <= 1e-2);
    }
}


int *ptr(char *name,
    int xs_len,
    int ys_len,
    float *xs,
    float *ys,
    float delta){
        printf("%s\n", name);
    // printf("xs_len = %d, ys_len=%d, delta=%f\n", xs_len, ys_len, delta);
    struct point_t *p_managed;
    int *ret_values_managed;
    size_t size = xs_len * ys_len;
    cudaMallocManaged(&p_managed, sizeof(point_t) * size);
    cudaMallocManaged(&ret_values_managed, sizeof(int) * size);
    for(int i = 0; i<xs_len; i++){
        for(int j = 0; j<ys_len; j++){
            int offset = i * ys_len + j;
            (p_managed + offset)->x = xs[i];
            (p_managed + offset)->y = ys[j];
            ret_values_managed[offset] = 0;
        }
    }
    int block_size = 256;
    int num_blocks = size / block_size + 1;

    if(strcmp(name, "line") == 0)
        line_kernel<<<num_blocks, block_size>>>(p_managed, ret_values_managed, size);
    else if(strcmp(name, "circle") == 0)
        circle_kernel<<<num_blocks, block_size>>>(p_managed, ret_values_managed, size);
    else if(strcmp(name, "ellipse") == 0)
        ellipse_kernel<<<num_blocks, block_size>>>(p_managed, ret_values_managed, size);
    else if(strcmp(name, "parabola") == 0)
        parabola_kernel<<<num_blocks, block_size>>>(p_managed, ret_values_managed, size);
    else if(strcmp(name, "hyperbola") == 0)
        hyperbola_kernel<<<num_blocks, block_size>>>(p_managed, ret_values_managed, size);
    else
        printf("todo: %s\n", name);

    cudaDeviceSynchronize();

    return ret_values_managed;
}

}

