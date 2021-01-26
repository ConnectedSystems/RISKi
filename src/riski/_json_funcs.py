"""RISKi - Additional class methods for JSON interaction."""
from typing import Dict, List
import sys
import json
from jsmin import jsmin

from sqlalchemy.orm import sessionmaker


def check_entry_exists(session, entry: Dict, schema_name: str, table: str):
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


def add_if_required(session, metadata, schema_name, table_name):
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
    elif num_entries == 1:
        rec_id = check_res[0]
    elif num_entries == 0:
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


def import_hazard_json(self, json_metadata_fn: str):
    """Import data with structure defined in provided JSON metadata file.

    Interfaces with the existing `rdl-data` code to do this.
    """
    import challenge_fund_db as cf
    from challenge_fund_db.hazard.generic_scenarios import JSONEventSet

    self._verbose_msg(f"Reading meta-data file {json_metadata_fn}\n")

    metadata = {}
    with open(json_metadata_fn, 'r') as fp:
        metadata = json.load(fp)

    es = JSONEventSet.from_md(metadata)

    self._verbose_msg("Importing event set")
    imported_id = cf.hazard.import_event_set(es)

    self._verbose_msg(f"Imported scenario DB id = {imported_id}")


def import_hazard_event(self, csv_fn, json_fn):
    self.insert_csv_data(csv_fn)
    self.import_hazard_json(json_fn)
    self._remove_temp_table()


def import_updated_hazard_json(self, json_metadata_fn: str):
    """Import JSON hazard data.

    Experimental work-in-progress for updated RDL schema.
    """
    import os
    import boto3
    from .schema import hazard

    self._verbose_msg(f"Reading meta-data file {json_metadata_fn}\n")

    with open(json_metadata_fn, 'r') as fp:
        minified = jsmin(fp.read())
        metadata = json.loads(minified)

    submission_name = metadata['name']
    crs = metadata['crs']
    # separate = ["name", "contribution", "events", "footprint_sets", "import_data", "crs"]

    event_set = metadata['event_set']
    contribution = metadata['contribution']
    events = metadata['events']
    footprint_sets = metadata['footprint_sets']
    footprint = metadata['footprint']
    import_data = metadata['import_data']  # collection of footprint_data

    Session = sessionmaker(bind=self.engine)
    session = Session()

    event_set_id = add_if_required(session, event_set, "hazard", "EventSet")

    contribution["event_set_id"] = event_set_id
    contribution_id = add_if_required(session, contribution, "hazard", "Contribution")

    events["event_set_id"] = event_set_id

    # TODO: For each table
    # Need to insert, and get corresponding ID to populate dependent table entries
    event_id = add_if_required(session, events, "hazard", "Event")

    footprint_sets["event_id"] = event_id
    footprint_set_id = add_if_required(session, footprint_sets, "hazard", "FootprintSet")

    footprint["footprint_set_id"] = footprint_set_id
    footprint_id = add_if_required(session, footprint, "hazard", "Footprint")

    # Connection to AWS S3
    # s3 = boto3.resource("s3")
    client = boto3.client('s3')

    # S3 bucket settings
    bucket = self.settings['aws-s3']['bucket_name']
    folder = self.settings['aws-s3']['folder']

    # Have to process data to be imported
    footprint_data = []
    for entry in import_data:

        import_format = entry['format']
        filename = entry['file']

        fname = filename.split(os.sep)[-1]
        uploaded_loc = f"{folder}/hazard/{fname}"

        # Upload data/file to S3 bucket or other upload location 
        # and get file_location.
        with open(filename, 'rb') as fp:
            client.upload_fileobj(fp, bucket, uploaded_loc)

        import_spec = {
            "footprint_id": footprint_id,
            "file_location": f"s3://{bucket}/{uploaded_loc}"
        }

        footprint_data.append(hazard.FootprintData(**import_spec))

    session.add_all(footprint_data)
    session.commit()
    session.flush()
    session.close()

