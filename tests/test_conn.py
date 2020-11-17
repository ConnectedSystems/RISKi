import pytest

import riski as rdi


def test_insertion():
    csv_fn = "data/CSVs/SWIO_COM_EQ_Shake_RP.csv"
    r_conn = rdi.RDLConnection(".settings.yaml", debug=True)

    r_conn.insert_csv_data(csv_fn)
