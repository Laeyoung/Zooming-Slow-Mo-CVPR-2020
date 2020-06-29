# 1. base image
FROM pytorch/pytorch:1.1.0-cuda10.0-cudnn7.5-devel

# 2. apt install
RUN apt update && \
  apt install -y git wget ffmpeg libsm6 libxext6 libxrender-dev libglib2.0-0

# 3. pip install
COPY ./pip.conf ~/.pip/pip.conf
RUN pip install numpy opencv-python lmdb pyyaml pickle5 matplotlib seaborn

# 4. install flask and expose 80 port
RUN pip install flask Flask-Limiter
EXPOSE 80

# 5. download pre-trained model
RUN mkdir /app
WORKDIR /app
RUN wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1xeOoZclGeSI1urY6mVCcApfCqOPgxMBK' -O model.pth

# 6. copy codes
COPY . .

# 7. set ENTRYPOINT and CMD
ENTRYPOINT bash /app/entrypoint.sh
CMD []
