from flask import Flask
from flask import render_template
from flask import jsonify
from flask import request
from flask_socketio import SocketIO, emit
import base64
from google_services import upload_blob, get_blobs
import sqlite3
import os
import subprocess
import time
import re
import asyncio
import websockets
import sys


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

connected_clients = set()

os.environ.setdefault("GCLOUD_PROJECT", "linen-server-399214")
if "dss-videos" not in os.listdir("/tmp"):
  os.mkdir("/tmp/dss-videos")

@app.route("/")
def index():
  return render_template('index.html', video_arg="video1694938174.mp4")

@app.route("/stream")
def stream():
  return render_template('stream.html')

@app.route('/video/<video_arg>')
def arguments_video(video_arg):
    return render_template('index.html', video_arg=video_arg)

   # return f"Here is the argument: {video_arg}"

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
  
@socketio.on('connect')
def handle_connect():
    print('Client connected')

async def video_stream(websocket, path):
    connected_clients.add(websocket)
    try:
        while True:
            frame_data = await websocket.recv()
            if frame_data == "stream_start":
                continue

            # Broadcast the frame to all connected clients
            for client in connected_clients:
                try:
                    await client.send(frame_data)
                except websockets.ConnectionClosed:
                    connected_clients.remove(client)
    except websockets.ConnectionClosed:
        connected_clients.remove(websocket)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    server = loop.create_server(websockets.serve(video_stream, '0.0.0.0/video_stream', 8080), host='0.0.0.0', port=8080)
    asyncio.ensure_future(server)
    socketio.run(app, host='0.0.0.0', port=8080, allow_unsafe_werkzeug=True)

