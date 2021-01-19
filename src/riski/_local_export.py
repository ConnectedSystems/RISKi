import os
import subprocess
import tempfile
import pandas as pd


test_export = """
SELECT
  rft.author_year as author_year,
  fc.id as id, 
  fc.hazard_type_primary as hazard_type_primary,
  fc.hazard_type_secondary as hazard_type_secondary,
  fc.process_type_primary as process_type_primary,
  fc.process_type_secondary as process_type_secondary,
  imt.im_code,
  imt.units,
  fc.occupancy as occupancy,
  fc.taxonomy_source as taxonomy_source,
  fc.taxonomy as taxonomy,
  fc.asset_type as asset_type,
  fc.asset_notes as asset_notes,
  fc.country_iso as country_iso,
  fc.applicability_notes as applicability_notes,
  fc.scale_applicability as scale_applicability,
  fc.function_type as function_type,
  fc.approach as approach,
  fc.f_relationship as f_relationship,
  fc.f_math as f_math,
  fc.f_math_model as f_math_model,
  fc.bespoke_model_ref as bespoke_model_ref,
  fc.f_reference as f_reference,
  fc.licence_code as licence_code,
  fc.licence_reference as licence_reference,
  fc.created_at as created_at
FROM mover.f_core fc
JOIN mover.f_specifics fsp on fc.id = fsp.f_specifics_id
JOIN mover.reference_table rft on rft.author_year = fc.f_reference
JOIN mover.f_additional fad on fad.f_additional_id = fsp.f_specifics_id
LEFT JOIN cf_common.imt imt on fsp.im_code = imt.im_code 
LEFT JOIN mover.damage_scale dmg on fsp.damage_scale_code = dmg.damage_scale_code
LEFT JOIN mover.edp_table edp on fsp.edp_code = edp.edp_code
LEFT JOIN mover.lp_table lp on fsp.lp_code = lp.lp_code
WHERE fc.id = 20
ORDER BY rft.author_year
"""


def read_sql_tmpfile(self, query):
    print("Test and development only!")

    with tempfile.TemporaryFile() as tmpfile:
        # Copy query results into CSV format, quoting special characters found in fields
        copy_sql = "COPY ({query}) TO STDOUT WITH CSV HEADER".format(
           query=query
        )

        with self.conn.cursor() as cur:
            cur.execute(query)

            cur.copy_expert(copy_sql, tmpfile)
            tmpfile.seek(0)
            df = pd.read_csv(tmpfile)

            str_cols = df.select_dtypes([object]).columns
            df.loc[:, str_cols] = df.loc[:, str_cols].replace("\\n", "\\\\n", regex=True)

            print(df)

        return df


def _export_exposure(self):
    print("For development only! Testing csv export issue with line terminator in string column")
    data = self.read_sql_tmpfile(test_export)
    data.to_csv('Murao_test_export.csv', index=False)
