from flask import Flask, jsonify, request, send_file
from queue import Empty, Queue
from flask_limiter import Limiter
from video_to_zsm import zsm

import os
import io
import numpy as np
import cv2
import io
import requests
import threading
import time 
import json
import subprocess

requests_queue = Queue()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 5

limiter = Limiter(app, default_limits=['1 per second'])

input_file_path = "/app/codes/input.mp4"
crop_file_path = "/app/codes/crop.mp4"
output_file_path = "/app/codes/output.mp4"

@app.route('/transfer', methods=['POST'])
def transfer():
  print("1 - /transfer API called.")

  if not request.files.get('input-video'):
    return {'error': 'must have a input video file'}, 400
  
  try:
    f = request.files['input-video']
    f.save(input_file_path)
    
    print("2 - resize and crop video (360p / 2 secs")
    os.system('{} -y -i {} -vf scale=360:-1 -ss 00:00:00 -t 00:00:02 {}'.format(os.path.join(ffmpeg_dir, "ffmpeg"), input_file_path, crop_file_path))
    
    print("2 - remove old output file")
    if os.path.exists(output_file_path):
      os.remove(output_file_path)
    else:
      print("Can not delete the file as it doesn't exists")
    
    print("3: Run zooming-slow-mo")
    output_video = zsm(input_file_path)
    
    print("4: Done")
    return send_file("/app/codes/" + output_video, mimetype='video/mp4')
  except Exception:
    return {'error': 'can not load your image files. check your image files'}, 400

@app.route('/health')
def health():
  return "ok"

@app.errorhandler(413)
def request_entity_too_large(error):
  return {'error': 'File Too Large'}, 413

@app.route('/')
def main(): 
  return app.send_static_file('index.html')

if __name__ == "__main__":
  app.run(debug=False, port=80, host='0.0.0.0')
  
