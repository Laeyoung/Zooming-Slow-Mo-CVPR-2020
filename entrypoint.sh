export CUDA_HOME=/usr/local/cuda-10.0
export CUDNN_INCLUDE_DIR=/usr/local/cuda-10.0/include
export CUDNN_LIB_DIR=/usr/local/cuda-10.0/lib64

cd /app/codes/models/modules/DCNv2

bash make.sh
