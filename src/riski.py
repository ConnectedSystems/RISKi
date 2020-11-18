from typing import Dict, List

import re
import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from _utils import load_settings

import ipdb


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
            conn_string = " ".join([f"{k}='{v}'" for (k, v) in rdl_db_settings.items()])

            self.conn = pg.connect(conn_string)
        else:
            rdl_db_settings = self.settings['database']['dev']
            conn_string = " ".join([f"{k}='{v}'" for (k, v) in rdl_db_settings.items()])
            self.conn = pg.connect(conn_string)

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
        tmp_df = pd.read_csv(csv_fn)

        columns = tmp_df.columns.tolist()

        # Extract datatype from DataFrame and strip numbers
        dtypes = tmp_df.dtypes.astype('string').tolist()
        dtypes = [re.sub('[0-9]+', '', d).replace('int', 'integer') for d in dtypes]

        struct = zip(columns, dtypes)

        self._create_temp_table(struct)

        st = [self._str_type(v) for k, v in struct]
        generated = ', '.join(st)

        query = "INSERT INTO {} VALUES ({})".format(self.tmp_table, generated)
        tmp_df.to_sql(query)

        return self

    def import_data(self):
        # insert data into temp table
        # generate JSON file describing data
        # 
        # Incorporate rdl-data scripts or simply do a subprocess call?
        pass

    def _str_type(self, form: str):
        """Interpret string to printf-style data type.

        Returns
        -------
        str, '%f', '%i', '%s' for float, integer, or string
        """
        form = form.lower()
        if form.startswith('f'):
            return '%f'
        elif form.startswith('i'):
            return '%i'
        elif form.startswith('s'):
            return '%s'
        else:
            raise ValueError(f"Unknown data type: {form}")

    def __del__(self):
        # Clean up on destruction

        self._remove_temp_table()  # remove table if exists
        self.conn.close()  # close connection


