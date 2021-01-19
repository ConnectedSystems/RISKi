from typing import Dict, List
from types import MethodType

import os
import re
import inspect

import psycopg2 as pg


import riski as ri
from riski._utils import load_settings, generate_config


def _test():
    pass