"""Import generated tiff files into local postgresql/postgis database.

geopackage details extracted with `gdalinfo [FILENAME].gpkg -json > data_details.json`
"""


@app.command()
def import_gpkg_rasters(settings_file: str, gpkg: str, dev: bool = False):
    """Import rasters from geopackage"""
    pass


# import os
# import json
# import subprocess

# with open("data_details.json") as fp:
#     details = json.loads(fp.read())

# sd_details = details['metadata']['SUBDATASETS']

# names = []
# for ent, sd in sd_details.items():
#     if ent.endswith('_NAME'):
#         names.append(sd)


# # Import each geotiff into postgis DB
# # base_cmd = "gdal_translate -ot Byte -of GTiff "

# # -I Create a GIST spatial index on the raster column.
# # -R register geotiff as out-of-database file
# base_cmd = "raster2pgsql -I -R"  # [CONVERTED FILENAME].gpkg | psql -U[USERNAME] -d [DATABASE NAME]
# conn = "dbname=shapefile_test user=testuser password=meowmeowbeans"
# for idx, n in enumerate(names):
#     infile = n.split(':')[-1]+".tiff"

#     # -R option requires absolute paths to be given
#     infile = os.path.abspath(infile)

#     if idx > 0:
#         cmd = f"{base_cmd} {infile} -a public.out_raster | psql \"{conn}\""
#     else:
#         cmd = f"{base_cmd} {infile} -c public.out_raster | psql \"{conn}\""

#     print(infile)
#     print(cmd)

#     subprocess.call(cmd, shell=True)
