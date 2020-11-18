

from riski._utils import load_settings
import typer
import glob
import subprocess



load_settings

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


    print(psql)

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

    # base_cmd = f"{psql} -h localhost -d {dbname} -U {user} < "
    subprocess.run(f"SET PGPASSWORD={pw}", shell=True)
    base_cmd = [psql, f"-d {dbname}", f"-U {user}", "<"]

    cmd = base_cmd + [f"{user_creator}"]
    print(cmd)
    # subprocess.run(cmd)

    # files should be ordered...
    for script in sql_files:
        cmd = base_cmd + [f"{script}"]
        # subprocess.run(cmd)
        print("would have called", cmd)


if __name__ == "__main__":
    app()