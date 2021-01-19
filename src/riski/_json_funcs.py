"""RISKi - Additional class methods for JSON interaction."""

import sys
import json

import challenge_fund_db as cf
from challenge_fund_db.hazard.generic_scenarios import JSONEventSet


def import_hazard_json(self, json_metadata_fn: str):
    """Import data with structure defined in provided JSON metadata file.

    Interfaces with the existing `rdl-data` code to do this.
    """
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
