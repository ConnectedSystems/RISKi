"""RISKi - Additional class methods for JSON interaction."""

import sys
import json
from jsmin import jsmin


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
    from .schema import hazard

    self._verbose_msg(f"Reading meta-data file {json_metadata_fn}\n")

    with open(json_metadata_fn, 'r') as fp:
        minified = jsmin(fp.read())
        metadata = json.loads(minified)

    separate = ["contribution", "events", "footprint_sets", "import_data"]

    event_set = {k: v for (k, v) in metadata.items() if k not in separate}
    contribution = metadata['contribution']
    events = metadata['events']
    footprint_sets = metadata['footprint_sets']
    import_data = metadata['import_data']

    new_eventset = hazard.EventSet(**event_set)
    new_contribution = hazard.Contribution(**contribution)
    new_event = hazard.Event(**events)
    new_footprint_sets = hazard.Event(**footprint_sets)

    # Have to process data to be imported
    # import_data...

