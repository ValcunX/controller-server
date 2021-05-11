from flask import Flask, render_template, request, abort
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os
import docker

load_dotenv()

app = Flask(__name__)
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

socketio = SocketIO(app)

client = docker.from_env()


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/test")
def test():
    if request.remote_addr != "127.0.0.1":
        abort(403)
    return render_template('test.html')


def print_status(message):
    emit('server_response', {
        'function': 'print_status',
        'args': {'message': message}
    }, json=True)


def redirect(url):
    emit('server_response', {
        'function': 'redirect',
        'args': {'url': url}
    }, json=True)


@socketio.on('open_project')
def open_project(req):
    pass


@socketio.on('close_project')
def close_project(req):
    pass


@socketio.on('create_volume')
def create_volume(req):
    pass


@socketio.on('duplicate_volume')
def duplicate_volume(req):
    pass


@socketio.on('delete_volume')
def delete_volume(req):
    pass


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
    socketio.run(app)
