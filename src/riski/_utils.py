from typing import Dict

import yaml

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