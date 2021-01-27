from typing import Dict, Union, List

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


def check_entry_exists(session, entry: Dict, schema_name: str, table: str) -> List[int]:
    """Queries target database for a matching entry.

    Generates query dynamically according to the given metadata entry.
    A downside of this approach is that the index is not utilized, so query
    performance may be comparably bad.

    On the positive side, it will follow the defined schema, as given in the
    metadata, so the query automatically adjusts as the schema spec changes.

    Parameters
    ----------
    session : SQLAlchemy session object
    entry : dict, metadata entry
    schema_name : str, name of schema
    table : str, name of table in schema to query

    Returns
    ----------
    List, of matching IDs
    """
    schema_def = f"{schema_name}.{table}"

    code = f"from .schema import {schema_name}\n\n"

    code += f"check = session.query({schema_def}.id).filter(\n"
    for k, v in entry.items():
        if k == "the_geom":
            # ignore geometry fields
            continue

        if isinstance(v, str):
            if (v.lower() not in ["true", "false"]):
                v = f"'{v}'"
            else:
                code += f"{schema_def}.{k}.is_({bool(v)}),\n"
        else:
            code += f"{schema_def}.{k} == {v},\n"


    code += ')'

    code_obj = compile(code, 'check_entry', 'exec')
    l = locals()
    exec(code_obj, globals(), l)

    check = l['check']

    return check.all()


def add_if_required(session, metadata: Dict, schema_name: str, table_name: str) -> int:
    """Inserts given metadata into table if a matching entry is not found.

    As with `check_entry_exists()`, the query automatically adjusts to the
    given schema.

    Parameters
    ----------
    session : SQLAlchemy session object
    metadata : dict, metadata entry 
    schema_name : str, name of schema
    table_name : str, name of table in schema to query

    Returns
    ----------
    int, ID of new or matching record
    """
    check_res = check_entry_exists(session, metadata, schema_name, table_name)
    num_entries = len(check_res)

    if num_entries > 1:
        raise RuntimeError("Found multiple records with same metadata!")

    try:
        rec_id = check_res[0]
    except IndexError:
        # entry does not exist yet
        stmt = f"from .schema import {schema_name}\n\n"
        stmt += f"new_entry = {schema_name}.{table_name}(**metadata)\n"
        stmt += f"session.add(new_entry)\n"
        stmt += f"session.flush()\n"
        stmt += f"rec_id = new_entry.id\n"

        l = locals()
        code_obj = compile(stmt, 'get_id', 'exec')
        exec(code_obj, globals(), l)
        rec_id = l['rec_id']

    return rec_id
