import base64
import io
import os
import sys
import cv2
import numpy as np
from PIL import Image

from detect import run
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('./index.html')


@app.route('/detectObject', methods=['POST'])
def mask_image():
	# print(request.files , file=sys.stderr)
    file = request.files['image'].read()
    npimg = np.fromstring(file, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    print(img.shape)
    cv2.imwrite("images/image.png",img)
    run(weights="best.pt",imgsz=660, source="images",project="results", name="",exist_ok=True, hide_conf=True,hide_labels=True, line_thickness=1)

    imageResults = cv2.imread("results/image.png",cv2.IMREAD_COLOR)
    is_sucess, bufImg = cv2.imencode(".png",imageResults)
    bytesImage = bufImg.tobytes()
    img_base64 = base64.b64encode(bytesImage)

    return jsonify({'status':str(img_base64)})

@app.after_request
def after_request(response):
    print("log: setting cors" , file = sys.stderr)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response

if __name__ == '__main__':
	app.run(debug = True)
