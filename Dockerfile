# 1. base image
FROM pytorch/pytorch:1.1.0-cuda10.0-cudnn7.5-devel

# 2. apt install
RUN apt update && \
  apt install -y git wget ffmpeg libsm6 libxext6 libxrender-dev libglib2.0-0

# 3. pip install
COPY ./pip.conf ~/.pip/pip.conf
RUN pip install numpy opencv-python lmdb pyyaml pickle5 matplotlib seaborn

# 4. clone repo and download pre-trained model
RUN git clone --recursive https://github.com/Laeyoung/Zooming-Slow-Mo-CVPR-2020.git && \
  mv Zooming-Slow-Mo-CVPR-2020 /app && \
  cd /app && \
  git checkout ainize && \
  git pull && \
  wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1xeOoZclGeSI1urY6mVCcApfCqOPgxMBK' -O model.pth

# . install flask and expose 80 port
RUN pip install flask Flask-Limiter
EXPOSE 80

#ENV CUDA_HOME /usr/local/cuda-10.0
#ENV CUDNN_INCLUDE_DIR /usr/local/cuda-10.0/include
#ENV CUDNN_LIB_DIR /usr/local/cuda-10.0/lib64

# 5. copy entrypoint.sh and set Docker ENTRYPOINT
#COPY ./entrypoint.sh /app/
#COPY ./app.py /app/
RUN chmod +x /app/entrypoint.sh && chmod +x /app/codes/app.py
WORKDIR /app
#ENTRYPOINT ["/app/entrypoint.sh"]
ENTRYPOINT bash /app/entrypoint.sh

CMD []
