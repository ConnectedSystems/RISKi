# RISKi - The [Risk] Data Library [i]nterface

An in-development package that provides a consistent programmatic front-end to interact with the Risk Data Library.


# Setup

The end goal is to make this a `pip` installable package.

For now, however, clone the repository and run:

```bash
pip install -e .
```

# Usage example

Create a `.settings.yaml` file specifying connection details.

These are being finalized but at a minimum:

```yaml
database:

  # Production server details
  rdl:
    dbname: rdl
    user: user
    password: password
    host: hostname
    port: 1234

  # The temporary table to create and upload data to 
  tmp_table: public.test_table

# Schema specific options
schemas:
  loss:
    OPTIONS:
      sslmode: require   # set to `prefer` for dev server

  hazard:
    OPTIONS:
      sslmode: require

  ged4all:
    OPTIONS:
      sslmode: require

# This is the location of the rdl-data project directories
# To avoid confusion, use absolute paths
# Ending slashes ('/') are recommended
rdl-data:
  sql: 'C:/programs/ownCloud/projects/rdl-data/sql/'
  python: 'C:/programs/ownCloud/projects/rdl-data/python/'
  challenge: 'C:/programs/ownCloud/projects/rdl-data/challenge_fund_db/'
  hazard: 'C:/programs/ownCloud/projects/rdl-data/challenge_fund_db/hazard/'
```

Generate config files for rdl-data

```bash
$ riski create-rdl-data-config .settings.yaml
```

### Programmatic Usage

```python
import riski as ri

r_conn = ri.RDLConnection(".settings.yaml")

csv_fn = "data/CSVs/SWIO_COM_EQ_Shake_RP.csv"
json_fn = "some_preformatted_metadata.json"

r_conn.import_hazard_event(csv_fn, json_fn)
```


### As a command-line tool:

```bash
# Generating config files for rdl-data
$ riski create-rdl-data-config .settings.yaml

# Edit JSON metadata file as needed

# Import hazard data
$ riski import-hazard .settings.yaml some_data.csv metadata.json
```


# Note

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
