from yaml import safe_load
from os import environ, path, curdir

def get_config():
    global config
    root_dir = path.abspath(curdir)
    env = environ.get('env', 'dev')
    with open(f'{root_dir}/env/{env}.yaml', 'r') as stream:
        config = safe_load(stream)
        return config