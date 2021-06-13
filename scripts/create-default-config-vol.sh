#! /bin/sh

config_vol="vulcanx_default_config"

echo "Deleting ${config_vol}"
eval "docker volume rm ${config_vol} || true"

echo "\nCreating ${config_vol}"
eval "docker volume create ${config_vol}"

echo "\nCopying default config files ${config_vol}"
eval "docker run -it --rm --name vulcanx_default_config -v $(pwd)/config:/from -v '${config_vol}':/to alpine cp -rav /from/. /to"

echo "\nCopied Files:"
eval "docker run -it --rm --name vulcanx_default_config -v $(pwd)/config:/from -v '${config_vol}':/to alpine ls -R /to"
