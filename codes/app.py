from flask import Flask, jsonify, request, send_file
from queue import Empty, Queue

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

@app.route('/health')
def health():
  return "ok"

@app.route('/')
def main(): 
  return app.send_static_file('index.html')

if __name__ == "__main__":
  app.run(debug=False, port=80, host='0.0.0.0')
  
