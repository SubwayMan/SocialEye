from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from google_services import upload_blob, get_blobs
import sqlite3
import os
import subprocess
import time
import re

app = Flask(__name__)
os.environ.setdefault("GCLOUD_PROJECT", "linen-server-399214")
if "dss-videos" not in os.listdir("/tmp"):
  os.mkdir("/tmp/dss-videos")


@app.route("/")
def index():
  return render_template('index.html')

@app.get('/video/<video_arg>')
def single_converter(video_arg):
    return "here is the + str(video_arg)"

@app.route("/video-index", methods=["GET"])
def video_index():
  # conn = sqlite3.connect("video_index.db")
  # c = conn.cursor()
  # c.execute("SELECT * FROM videos")
  # rows = c.fetchall()
  # conn.close()
  items = []
  for name in get_blobs():
    items.append(name)
  return jsonify({"items": items}), 200

  
@app.route("/video-upload", methods=["POST"])
def video_upload():
  assert "video" in request.files, "No file part"
  video = request.files["video"]
  
  assert video.filename, "No selected file"
  video_name = video.filename.split(".")[0]

  print(request.text)


  video_path = f"/tmp/dss-videos/{video.filename}"
  print(video_path)
  with open(video_path, "wb") as f:
    f.write(video.read())

  print(os.listdir("/tmp/dss-videos"))

  newpath = f"/tmp/dss-videos/{video_name}.mp4"
  subprocess.run(["ffmpeg", "-framerate", "24", "-i", video_path, "-c", "copy", newpath])
  
  new_video = open(newpath, "rb")
  newpath = os.path.join("videos", newpath.split("/")[-1])

  public_url = upload_blob(new_video, video_name, newpath)
  print("Public url:", public_url)
  print("I just created ", video_name, newpath)
  
  # conn = sqlite3.connect("video_index.db")
  # c = conn.cursor()
  # timestamp = int(re.search(r"\d+", video_name).group(0))
  # c.execute("INSERT INTO videos (name, url, length, timestamp) VALUES (?, ?, ?, ?)", (video_name, public_url, 60, timestamp))
  # conn.commit()
  # conn.close()
  
  return "File upload successful", 200
  
app.run(host='0.0.0.0',port=8080)
