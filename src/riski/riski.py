from typing import Dict, List

import re
import psycopg2 as pg
from sqlalchemy import create_engine

import numpy as np
import pandas.io.sql as psql
import pandas as pd


from ._utils import load_settings


class RDLConnection(object):

    def __init__(self, settings: str, tmp_table: str = 'tablename', dev: bool = False):
        """Constructor for RDLConnection.

        Parameters
        ----------
        settings : str,
            Path to settings file in yaml format.

        tmp_table : str (default: 'tablename'),
            name of temporary table to use
        
        dev : bool (default: False),
            Whether to use local development server or not.

        """

        # Load in settings
        self.settings = load_settings(settings)
        self.tmp_table = tmp_table

        # Establish connection to DB
        if not dev:
            rdl_db_settings = self.settings['database']['rdl']

            user = rdl_db_settings['user']
            password = rdl_db_settings['password']
            host = rdl_db_settings['host']
            port = rdl_db_settings['port']
            dbname = rdl_db_settings['dbname']

            conn_string = " ".join([f"{k}='{v}'" for (k, v) in rdl_db_settings.items()])
            self.conn = pg.connect(conn_string)

            # conn_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
            # self.conn = create_engine(conn_string)


        else:
            rdl_db_settings = self.settings['database']['dev']
            conn_string = " ".join([f"{k}='{v}'" for (k, v) in rdl_db_settings.items()])
            self.conn = pg.connect(conn_string)

            print("Connected to local dev server")


    def _create_temp_table(self, struct):
        """Create a temporary table for the data import.

        Parameters
        ----------
        struct : List[tuple],
            Table column structure in the form of [("column name", "data type"), ]
        """
        columns = ",\n".join([f"{k} {v}" for k, v in struct])
        query = """CREATE TABLE {}({})""".format(self.tmp_table, columns)

        with self.conn.cursor() as cur:
            cur.execute(query)

    def _remove_temp_table(self):
        """Deletes temporary table from database."""
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS {}".format(self.tmp_table))
    
    def insert_csv_data(self, csv_fn: str):
        """Insert CSV data into temporary table.

        Parameters
        ----------
        csv_fn : str,
            filepath to CSV data file
        """
        tmp_df = pd.read_csv(csv_fn, skipinitialspace=True)

        columns = tmp_df.columns.tolist()
        self._ensure_location(columns)

        # Extract datatype from DataFrame and strip numbers
        dtypes = tmp_df.dtypes.astype('string').tolist()
        dtypes = [re.sub('[0-9]+', '', d).replace('int', 'integer') for d in dtypes]

        struct = list(zip(columns, dtypes))

        self._create_temp_table(struct)

        st = [self._str_type(v) for k, v in struct]

        if len(st) == 0:
            raise ValueError("Empty structure for CSV (could not determine data types)")

        generated = ', '.join(st)
        columns = ', '.join(columns)

        with np.printoptions(threshold=np.inf):
            values = str(tmp_df.to_records(index=False)).replace('[', '').replace(']', '').replace('\n', ',\n')

        query = f"INSERT INTO {self.tmp_table}({columns}) VALUES {values}"

        with self.conn.cursor() as cur:
            cur.execute(query)

        return self

    def import_data(self):
        # insert data into temp table
        # generate JSON file describing data
        # 
        # Incorporate rdl-data scripts or simply do a subprocess call?
        pass

    def run_query(self, query):
        with self.conn.cursor() as cur:
            cur.execute(query)
            # print(cur.rowcount, "rows inserted")

        return self

    def _str_type(self, form: str):
        """Interpret string to printf-style data type.

        Returns
        -------
        str, '%f', '%i', '%s' for float, integer, or string
        """
        form = form.lower()
        if form.startswith('f'):
            return r'%f'
        elif form.startswith('i'):
            return r'%i'
        elif form.startswith('s'):
            return r'%s'
        else:
            raise ValueError(f"Unknown data type: {form}")
    
    def _ensure_location(self, columns):
        location_id = "LocID" in columns
        lon = "lon" in columns
        lat = "lat" in columns
        
        if location_id and lon and lat:
            return

        raise ValueError("Provided CSV does not specify LocID, lon, or lat\n{}".format(columns))

    def __del__(self):
        # Clean up on destruction

        self._remove_temp_table()  # remove table if exists
        self.conn.close()  # close connection


