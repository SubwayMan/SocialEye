from flask import Flask
from flask import jsonify
from flask import request
from google_services import upload_blob
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/video-index", methods=["GET"])
def video_index():
  return jsonify({})

@app.route("/video-upload", methods=["POST"])
def video_upload():
  assert "video" in request.files, "No file part"
  video = request.files["video"]
  
  assert video.filename, "No selected file"
  video_name = video.filename
  video_path = f"videos/{video_name}"

  upload_blob(video, video_path)
  
  return "File upload successful", 200
  
app.run(host='0.0.0.0',port=8080)
