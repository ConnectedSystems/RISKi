# RISKi - The [Risk] Data Library [i]nterface

An in-development package that provides a consistent programmatic framework for the Risk Data Library.

For historic reasons, the current implementation depends on:

* rdl-data
* rdl-infra (for local development)

Work is in process to slowly replace the functionality provided by these packages.

# Setup

The end goal is to make this a `pip` installable package.

For now, however, clone the repository and run:

```bash
$ conda create -n gfdrr-rdl --file windows_env.yml
$ pip install -e .
```

# Usage example

Create a `.settings.yaml` file specifying DB connection details.

This provides backwards compatibility with the `rdl-*` packages where needed.

These are being finalized but at a minimum:

```yaml
database:

  # development server details 
  # (can put in multiple entries)
  dev:
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
# (a long-term goal is to make this no longer required)
rdl-data:
  sql: C:/example/rdl-data/sql/
  python: C:/example/rdl-data/python/
  challenge: C:/example/rdl-data/challenge_fund_db/
  hazard: C:/example/rdl-data/challenge_fund_db/hazard/
```

Generate config files for rdl-data

```bash
$ riski create-rdl-data-config dev
```

### Programmatic Usage

```python
# Create schema on local DB
import riski as ri

r_conn = ri.RDLConnection(".settings.yaml", db_name='dev')
r_conn.create_schema()
```

```python
import riski as ri

r_conn = ri.RDLConnection(".settings.yaml", db_name='dev')

json_fn = "some_preformatted_metadata.json"
r_conn.import_hazard_json(json_fn)
```


### As a command-line tool:

```bash
# If setting up local DB
$ riski setup-dev-db

# Generating config files for rdl-data
# Format is: riski [command] [database name]
$ riski create-rdl-data-config dev

# Edit JSON metadata file as needed

# Import hazard data
$ riski import-hazard dev metadata.json
```


# Note

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.


## Errors

On Windows, you may run into an error: `FileNotFoundError: Could not find module '... geos_c.dll' (or one of its dependencies). Try using the full path with constructor syntax.'`

This is caused by, we think, shapely not including the referenced `.dll` file in its installation (via pip). The (temporary) solution is to copy the `.dll` into the expected location.
