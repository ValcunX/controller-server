docker run --rm -it --name valcunx_controller-server --env-file ./.env.prod -p 5051:80 -p 5052:5050 -v "/var/run/docker.sock":"/var/run/docker.sock" -v $(pwd):/app vulcanx/controller-server
