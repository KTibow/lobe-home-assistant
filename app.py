from flask import Flask, request
from lobe import ImageModel
from PIL import Image, ImageFile
import io
from base64 import b64decode

app = Flask(__name__)
model = ImageModel.load("/home/pi/model/")

@app.route("/predict", methods=["POST"])
def predict():
  img = request.get_json(force=True)
  img = img.get("image")
  image_object = bytearray(b64decode(img))
  image_object = io.BytesIO(image_object)
  image_object = Image.open(image_object).convert("RGB")
  prediction = model.predict(image_object).as_dict()
  print(prediction)
  return prediction

app.run(host="0.0.0.0", port="5623")
