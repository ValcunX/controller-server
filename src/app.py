from flask import Flask, render_template, request, abort
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from dotenv import load_dotenv
import os
import docker
import time

load_dotenv()

app = Flask(__name__)
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
CORS(app)

socketio = SocketIO(app, cors_allowed_origins="*")

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
    try:
        print_status(f"Starting Container for Project: {req['name']}")
        name = f"code-server-{req['id']}"
        port = 10000 + int(req['id'])
        req['volume_id'] = os.getcwd() if req['volume_id'] == "" else req['volume_id']
        # TODO: Change this to volume
        print(os.path.join(os.getcwd(), 'config'))
        container = client.containers.run(req["language"]["image_id"], detach=True, 
                                        hostname=name, name=name, 
                                        volumes={
                                            os.getenv('CONFIG_VOL'): {'bind': '/home/coder/.config', 'mode': 'ro'},
                                            # TODO: User perms
                                            req['volume_id']: {'bind': '/home/coder/project', 'mode': 'rw'},
                                        },
                                        ports={"8080": port})

        while container.status != "running":
            time.sleep(1)
            print_status(f'Logs:\n{container.logs().decode("utf-8")}\nStarted Container')
            container.reload()
        
        time.sleep(2)
        print_status(f'Logs:\n{container.logs().decode("utf-8")}\nStarted Container')
        print_status(f'Goto <a href="http://localhost:{port}/">http://localhost:{port}/</a>')
        # TODO: Redirect user

        return port
    except Exception as ex:
        print_status(f'Error: {str(ex)}')
    return None

@socketio.on('close_project')
def close_project(req):
    try:
        print_status(f"\nStopping Container for Project: {req['name']}")
        name = f"code-server-{req['id']}"
        container = client.containers.get(name)
        print_status(f'Logs:\n{container.logs().decode("utf-8")}')
        container.kill()
        container.remove()
        print_status("Stopped Container.\n")
        
        return True
    except Exception as ex:
        print_status(f'Error: {str(ex)}')
    return False

@socketio.on('create_volume')
def create_volume():
    try:
        print_status(f"Creating Volume")
        volume = client.volumes.create()
        name = f"vol-create-for_{volume.name[:6]}"
        print_status(f"1, {name}")

        container = client.containers.run("alpine", detach=False, stream=True, remove=True, name=name, 
                                        volumes = {volume.name: {'bind': '/vol', 'mode': 'rw'}},
                                        entrypoint='chown 1000:1000 /vol')
        print_status(f"2")
        # for log in container:
        #     print_status(f'Logs:\n{log.decode("utf-8")}')
        
        print_status(f"Created Volume: {volume.name}")
        return volume.name
    except Exception as ex:
        print(ex)
        print_status(f'Error: {str(ex)}')
    return None


@socketio.on('duplicate_volume')
def duplicate_volume(vol_id):
    try:
        print_status(f"Creating Volume")
        dest_vol = client.volumes.create()
        name = f"vol-dup-for-dest_{dest_vol.name[:6]}"
        print_status(f"Created Volume: {dest_vol.name}\nStarted copying data from {vol_id} to {dest_vol.name}")
        
        container = client.containers.run("alpine", detach=False, stream=True, remove=True, name=name, 
                                        volumes={
                                            vol_id: {'bind': '/from', 'mode': 'rw'},
                                            dest_vol.name: {'bind': '/to', 'mode': 'rw'},
                                        },
                                        entrypoint='cp -rav /from/. /to')
        for log in container:
            print_status(f'Logs:\n{log.decode("utf-8")}')

        print_status(f"{vol_id} duplicated to {dest_vol.name}")
        return dest_vol.name
    except Exception as ex:
        print_status(f'Error: {str(ex)}')
    return None

@socketio.on('delete_volume')
def delete_volume(vol_id):
    try:
        print_status(f"Deleting Volume")
        volume = client.volumes.get(vol_id)
        volume.remove()
        print_status(f"Deleted Volume: {volume.name}")
        
        return volume.name
    except Exception as ex:
        print_status(f'Error: {str(ex)}')
    return None


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
    socketio.run(app)
