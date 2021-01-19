from typing import Dict, Union

from os.path import join as pj

import yaml
import json

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def load_settings(fn: str) -> Dict:
    """Loads settings given in a YAML file.
    
    Parameters
    ----------
    fn : str,
        Path to YAML file to load

    Returns
    ----------
    dict, of database settings
    """
    with open(fn) as fp:
        settings = yaml.load(fp, Loader=Loader)
    
    return settings


def generate_config(settings: Union[str, Dict], db_name: str):
    """rdl-data interface - generate dictionary configuration.

    TODO: Move this function elsewhere...
    """
    if isinstance(settings, str):
        settings = load_settings(settings)

    schema_settings = settings['schemas']
    db_settings = settings['database'][db_name]

    # target path
    cf = settings['rdl-data']['challenge']

    for schema_name, config in schema_settings.items():
        path = pj(cf, schema_name, 'db_settings.py')

        tp = {
            f'{schema_name}_reader': {
                'NAME': db_settings['dbname'],
                'USER': db_settings['user'],
                'PASSWORD': db_settings['password'],
                'HOST': db_settings['host'],
                'PORT': db_settings['port'],
                'OPTIONS': config['OPTIONS']
            },
            f'{schema_name}_contrib': {
                'NAME': db_settings['dbname'],
                'USER': db_settings['user'],
                'PASSWORD': db_settings['password'],
                'HOST': db_settings['host'],
                'PORT': db_settings['port'],
                'OPTIONS': config['OPTIONS']
            }
        }

        with open(pj(cf, schema_name, 'db_settings.py'), 'w') as fp:
            fp.write('db_confs = '+json.dumps(tp, indent=4))
    
