# Local RDL Dev Server Setup

This document provides a guide for setting up a local development server for the Risk Data Library and the RISKi package.

Prerequisites:

Download and install PostgreSQL 13 and a DB client of your choice.

The PostgreSQL installer comes with pgAdmin, and the instructions here assumes this is being used.

https://www.postgresql.org/download/windows/

When prompted, install StackBuilder as well.

During the StackBuilder installation process, it will give you the option of installing further extensions for PostgreSQL.
Select and install the PostGIS 3.0 Bundle (located under "Spatial Extensions").

This guide assumes you already have cloned the [`rdl-data` project](https://github.com/GFDRR/rdl-data)


Note:

It will ask for a master password for the superuser `postgres`.
DO NOT FORGET THIS PASSWORD (otherwise you will have to reinstall).

Take note of where PostgreSQL is installed - this information is necessary later when creating/importing data.

It will ask about the following options. 

- No need to create a spatial database at this stage
- It will ask to register GDAL_DATA. Say "No" - Do not overwrite local GDAL settings
- Raster drivers are disabled by default. Enable? Say "yes".
- Raster out of db is disabled by default. Enable? Say "yes".

Once installation is complete, start pgAdmin and set the master password for pgAdmin when prompted.
This can be different from the `postgres` user password.

## Server and Database creation

Here is a step-by-step guide for Windows:

1. Open pgAdmin
2. Right-click on "Servers" on the left-hand panel and select "Create Server"
3. In the "General" tab give the dev server a name (e.g. `rdl-dev`).
4. In the "Connection" tab, specify the options as below:

```
Hostname/address: localhost
Port: 5432
Maintenance database: postgres (i.e. leave it as is)
Username: postgres
Password: <your master password for user 'postgres'>
```

### Create a user for the development server.

1. Right-click on the just created server "rdl-dev" -> Create -> Login/Group Role
2. Give the user a name (e.g. `testuser`)
3. "Definition" tab: provide a password
4. Privileges tab: 
   1. Can login -> Yes
   2. Create roles -> Yes
   3. Create databases -> Yes
   4. Is superuser -> Yes

### Create a database

1. Right-click on the "rdl-dev" server -> Create -> Database
2. Name the database (e.g. "rdl-dev")


## Run SQL scripts from rdl-data

If not yet created, make a `.settings.yaml` file somewhere, preferably in the RISKi project directory.

Add the details the `.settings.yaml` file in the following format (I used mine as an example):

```yaml
database:
  dev:
    dbname: rdl-dev  # this is the database name you provided
    user: testuser
    password: meowmeowbeans
    host: localhost
    port: 5432

  # Location of the psql.exe file
  psql: C:/Program Files/PostgreSQL/13/bin/psql.exe

# This is the location of the rdl-data project directories
rdl-data:
  sql: 'C:/programs/ownCloud/projects/rdl-data/sql'
  python: 'C:/programs/ownCloud/projects/rdl-data/python'
  challenge: 'C:/programs/ownCloud/projects/rdl-data/challenge_fund_db'
  hazard: 'C:/programs/ownCloud/projects/rdl-data/challenge_fund_db/hazard'
```



### Run script to create database

```bash
riski setup-dev-db .settings.yaml
```
