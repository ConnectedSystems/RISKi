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
```

### Programmatic Usage

```python
import riski as ri

r_conn = ri.RDLConnection(".settings.yaml", dev=True)

csv_fn = "data/CSVs/SWIO_COM_EQ_Shake_RP.csv"
r_conn.insert_csv_data(csv_fn)
```


### As a command-line tool:

```bash
# To import hazard data
$ riski import-hazard .settings.yaml some_data.csv metadata.json
```



# Note

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
