import json as js
import typer
import riski as ri


r_conn = ri.RDLConnection(".settings.yaml", db_name='dev')
app = typer.Typer()


@app.command()
def json(schema: str):

    # from riski.schema import hazard
    # from riski.schema import Base
    from sqlalchemy import inspect

    inspector = inspect(r_conn.engine)
    schemas = inspector.get_schema_names()

    assert schema in schemas, "Schema ({schema}) not valid."

    # TODO: Generate JSON template from Schema details
    # template = {"name": ""}
    # tables = inspector.get_table_names(schema=schema)

    template = """// see http://www.riskdatalibrary.org/documentation for further details
{
    "name": "",  //this field is ignored - a human-understandable name for this submission
    "event_set": {
        "description": "",
        "creation_date": "",
        "bibliography": "",
        "hazard_type": "",
        "geographic_area_name": "",
        "is_prob": ""  //True or False
    },
    "contribution": {
        "component": "Hazard",
        "model_date": "",
        "model_source": "",
        "notes": "",
        "version": "",
        "project": "",
        "license_code": "",
        "purpose": "",
        "geo_coverage": "",
        "contributed_at_timestamp": ""
    },
    "event": {
        "calculation_method": "",
        "description": ""
    },
    "footprint_sets": {
        "imt": "",
        "process_type": ""
    },
    "footprint": {
        "uncertainty_2nd_moment": null,
        "trigger_footprint_id": null
    },
    "footprint_data": [  // list of geotiffs to be imported
        {
            "file": ""
        }
    ]
}
    """

    with open("rdl-hazard-template.jsonc", 'w') as fp:
        fp.write(template)

    typer.echo("Created JSON template for hazard.")