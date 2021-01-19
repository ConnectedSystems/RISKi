"""RISKi - Additional class methods for XML interaction."""

import sys
import json

import challenge_fund_db as cf
from challenge_fund_db.ged4all.import_exposure_nrml import import_exposure_file


def import_exposure_event(self, xml_fn):
    self._verbose_msg("Importing {0}\n".format(xml_fn))
    imported_id = import_exposure_file(xml_fn)
    
    self._verbose_msg(f"Imported scenario DB id = {imported_id}")

    # log msg (not yet implemented)
    # self._log("Imported model DB id = {0}\n".format(imported_id))
