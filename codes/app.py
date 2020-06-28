from flask import Flask, jsonify, request, send_file
from queue import Empty, Queue
from flask_limiter import Limiter
from video_to_zsm import zsm

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

@app.route('/transfer', methods=['POST'])
def transfer():

  if not request.files.get('input-video'):
    return {'error': 'must have a input video file'}, 400

  try:
    input_video = Image.open(request.files['base_image'].stream)

    output_video = zsm(input_video)

    return send_file(output_video, mimetype='video/mp4')
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
  
