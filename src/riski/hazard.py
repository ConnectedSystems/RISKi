"""RISKi - Additional class methods for handling hazard data."""

from typing import Dict, List
import sys
import json
from jsmin import jsmin

from sqlalchemy.orm import sessionmaker

from ._utils import add_if_required, extract_bounds


def import_hazard_json(self, json_metadata_fn: str):
    """Import JSON hazard data.

    Experimental work-in-progress for updated RDL schema.
    """
    import os
    import boto3
    from .schema import hazard

    import rasterio
    from shapely.geometry import box


    self._verbose_msg(f"Reading meta-data file {json_metadata_fn}\n")

    with open(json_metadata_fn, 'r') as fp:
        minified = jsmin(fp.read())
        metadata = json.loads(minified)

    event_set = metadata['event_set']
    contribution = metadata['contribution']
    event = metadata['event']
    footprint_sets = metadata['footprint_sets']
    footprint = metadata['footprint']
    import_data = metadata['footprint_data']  # collection of footprint_data

    # S3 bucket settings
    bucket = self.settings['aws-s3']['bucket_name']
    folder = self.settings['aws-s3']['folder']

    session = sessionmaker(bind=self.engine)()

    # Connection to AWS S3
    client = boto3.client('s3')

    # Determine maximum extent
    footprint_data = []
    geoms = []
    folder_prefix = f"{folder}/hazard/"
    for entry in import_data:
        filename = entry['file']

        fname = filename.split(os.sep)[-1]

        fileformat = entry['format']

        bounds = extract_bounds(filename, fileformat)
        geoms.append(bounds)
        

        uploaded_loc = f"{folder_prefix}/{fname}"

        # Upload data/file to S3 bucket or other upload location 
        # and get file_location.
        with open(filename, 'rb') as fp:
            client.upload_fileobj(fp, bucket, uploaded_loc)

        footprint_data.append({
            "file_location": f"s3://{bucket}/{uploaded_loc}"
        })

    # Determine maximum extent
    unified_geom = geoms[0]
    for g in geoms[1:]:
        unified_geom = unified_geom.union(g)

    event_set['the_geom'] = str(unified_geom)
    event_set_id = add_if_required(session, event_set, "hazard", "EventSet")

    contribution["set_id"] = event_set_id
    contribution_id = add_if_required(session, contribution, "common", "Contribution")

    event["event_set_id"] = event_set_id

    event_id = add_if_required(session, event, "hazard", "Event")

    footprint_sets["event_id"] = event_id
    footprint_set_id = add_if_required(session, footprint_sets, "hazard", "FootprintSet")

    footprint["footprint_set_id"] = footprint_set_id
    footprint_id = add_if_required(session, footprint, "hazard", "Footprint")

    for ft in footprint_data:
        ft['footprint_id'] = footprint_id

    footprint_data = [hazard.FootprintData(**import_spec) 
                      for import_spec in footprint_data]

    session.add_all(footprint_data)
    session.commit()
    session.flush()
    session.close()

