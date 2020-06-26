FROM pytorch/pytorch:1.1.0-cuda10.0-cudnn7.5-devel

RUN apt update && \
  apt install -y git wget && \
  git clone --recursive https://github.com/Mukosame/Zooming-Slow-Mo-CVPR-2020.git && \
  mv Zooming-Slow-Mo-CVPR-2020 /app && \
  apt-get install -y libsm6 libxext6 libxrender-dev libglib2.0-0 && \
  pip install numpy opencv-python lmdb pyyaml pickle5 matplotlib seaborn jupyterlab && \
  cd /app && \
  wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1xeOoZclGeSI1urY6mVCcApfCqOPgxMBK' -O model.pth

COPY ./entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]

WORKDIR /app

CMD []
