import os
from .app import app
from .app import socketio
from flask_cors import CORS

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

if __name__ == "__main__":
    CORS(app)
    app.run()
    socketio.run(app)
