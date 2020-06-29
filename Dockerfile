# 1. base image
FROM pytorch/pytorch:1.1.0-cuda10.0-cudnn7.5-devel

# 2. apt install
RUN apt update && \
  apt install -y git wget ffmpeg libsm6 libxext6 libxrender-dev libglib2.0-0

# 3. pip install
COPY ./pip.conf ~/.pip/pip.conf
RUN pip install numpy opencv-python lmdb pyyaml pickle5 matplotlib seaborn

# . install flask and expose 80 port
RUN pip install flask Flask-Limiter
EXPOSE 80

RUN mkdir /app
WORKDIR /app

# 4. download pre-trained model
RUN wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1xeOoZclGeSI1urY6mVCcApfCqOPgxMBK' -O model.pth

# 5. copy codes
COPY . .

#ENV CUDA_HOME /usr/local/cuda-10.0
#ENV CUDNN_INCLUDE_DIR /usr/local/cuda-10.0/include
#ENV CUDNN_LIB_DIR /usr/local/cuda-10.0/lib64

# 5. copy entrypoint.sh and set Docker ENTRYPOINT
#COPY ./entrypoint.sh /app/
#COPY ./app.py /app/
#RUN chmod +x /app/entrypoint.sh && chmod +x /app/codes/app.py

ENTRYPOINT bash /app/entrypoint.sh

CMD []
