'''Command-line utility for RISKi'''

import glob
import subprocess
import os

import typer

from riski._utils import load_settings


app = typer.Typer()


@app.command()
def setup_dev_db(settings_file: str):
    settings = load_settings(settings_file)
    data_settings = settings['rdl-data']

    sql_dir = data_settings['sql']
    sql_files = glob.glob(f"{sql_dir}/*.sql")
    sql_files = [glob.escape(s) for s in sql_files]

    psql = settings['database']['psql']
    dev_settings = settings['database']['dev']

    # Find user creation script
    user_script = "create-users.sql"

    user_script_index = [i for i, s in enumerate(sql_files) if user_script in s]
    if len(user_script_index) > 1:
        raise ValueError("Found more than one user creation script!")
    if len(user_script_index) == 0:
        raise ValueError("Could not find user creation script!")

    user_creator = sql_files.pop(7)

    dbname = dev_settings['dbname']
    user = dev_settings['user']
    pw = dev_settings['password']

    if 'PGPASSWORD' not in os.environ:
        os.environ['PGPASSWORD'] = pw

    base_cmd = [psql, f"-U{user}", f"-d{dbname}"]
    cmd = base_cmd + [f"-f{user_creator}"]
    subprocess.run(cmd)

    # files should be ordered...
    for script in sql_files:
        cmd = base_cmd + [f"-f{script}"]
        subprocess.run(cmd)


@app.command()
def test():
    print("yes")

def main():
    app()


if __name__ == '__main__':
    app()