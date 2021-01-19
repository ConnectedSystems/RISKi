import pytest

import riski as ri


@pytest.mark.xfail(reason="JSON missing commas")
def test_malformed_import():
    r_conn = ri.RDLConnection(".settings.yaml", db_name='dev')

    csv_fn = "data/CSVs/SWIO_COM_EQ_Shake_RP.csv"
    json_fn = "data/JSONs/malformed.json"

    r_conn.import_hazard_event(csv_fn, json_fn)

@pytest.mark.xfail(reason="No DB on travis")
def test_hazard_import():

    r_conn = ri.RDLConnection(".settings.yaml", db_name='dev')

    csv_fn = "data/CSVs/SWIO_COM_EQ_Shake_RP.csv"
    json_fn = "data/JSONs/com-eq-qgm.json"

    r_conn.import_hazard_event(csv_fn, json_fn)
    r_conn._remove_temp_table()
    


if __name__ == '__main__':
    test_hazard_import()
