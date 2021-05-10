from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import time, os, socket
import docker

load_dotenv()

app = Flask(__name__)
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

socketio = SocketIO(app)

@app.route("/")
def index():
    return "<h1>Hello, This is ValcunX Docker Controller Server. :)</h1>"

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
    socketio.run(app)
