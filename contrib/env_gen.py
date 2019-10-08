#!/usr/bin/env python

"""
Django SECRET_KEY generator.
"""
import sys

from django.utils.crypto import get_random_string


chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"

CONFIG_STRING = """
DEBUG=True
SECRET_KEY={}
ALLOWED_HOSTS=127.0.0.1, .localhost
DBNAME=
DBUSER=
DBPASS=
DBIPHOST=
DBPORT=
""".strip().format(
    get_random_string(50, chars)
)

# Writing our configuration file to '.env'
with open(".env", "w") as configfile:
    configfile.write(CONFIG_STRING)
