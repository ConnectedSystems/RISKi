import pytest

import riski as ri


def test_insertion():
    csv_fn = "data/CSVs/SWIO_COM_EQ_Shake_RP.csv"
    r_conn = ri.RDLConnection(".settings.yaml", dev=False)

    r_conn.insert_csv_data(csv_fn)


if __name__ == '__main__':
    test_insertion()
