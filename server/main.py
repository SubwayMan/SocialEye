from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from google_services import upload_blob
import sqlite3
import time

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/video-index", methods=["GET"])
def video_index():
  conn = sqlite3.connect("video_index.db")
  c = conn.cursor()
  c.execute("SELECT * FROM videos")
  rows = c.fetchall()
  conn.close()
  return jsonify(rows)
  
@app.route("/video-upload", methods=["POST"])
def video_upload():
  assert "video" in request.files, "No file part"
  video = request.files["video"]
  
  assert video.filename, "No selected file"
  video_name = video.filename
  video_path = f"videos/{video_name}"

  public_url = upload_blob(video, video_name, video_path)
  
  conn = sqlite3.connect("video_index.db")
  c = conn.cursor()
  c.execute("INSERT INTO videos (name, url, length, timestamp) VALUES (?, ?, ?, ?)", (video_name, public_url, 60, int(time.time())))
  conn.commit()
  conn.close()
  
  return "File upload successful", 200
  
app.run(host='0.0.0.0',port=8080)
