"""Incomplete - only to showcase possible approach to JSON template editing."""

from riski._utils import load_settings
import typer
import glob
import subprocess

import json

from io import StringIO


app = typer.Typer()

@app.command()
def create(template_file: str):

    schema = typer.prompt("What schema is this for?")

    with open(template_file, 'r') as fp:
        template = json.load(fp)

    print(template['geographic_area_name'])

    geographic_area_name = typer.prompt("Geographic name")
    template['geographic_area_name'] = geographic_area_name

    typer.echo(f"Geo location set to {template['geographic_area_name']}")

    json_string = json.dumps(template, indent=2)

    tablename = typer.prompt("Target table name")
    json_string = json_string.replace('[tablename]', tablename)

    template = json.loads(json_string.replace('\n', ''))
    
    print(json.dumps(template, indent=2))
    




if __name__ == "__main__":
    app()
