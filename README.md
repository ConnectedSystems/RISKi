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
  rdl:
    dbname: rdl
    user: user
    password: password
    host: hostname
    port: 1234
```


```python
import riski as ri

csv_fn = "data/CSVs/SWIO_COM_EQ_Shake_RP.csv"
r_conn = ri.RDLConnection(".settings.yaml", debug=True)

r_conn.insert_csv_data(csv_fn)
```


# Note

This project has been set up using PyScaffold 3.2.3. For details and usage
information on PyScaffold see https://pyscaffold.org/.
