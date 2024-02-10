#!usr/bin/python3

""" An initialization file"""

from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
