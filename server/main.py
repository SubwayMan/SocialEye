from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("video-index")
def video_index():
  return jsonify({})
  
app.run(host='0.0.0.0',port=8080)
