#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
# from models.engine.file_storage import FileStorage
from os import getenv


if getenv("HBNB_TYPE_STORAGE") == "db":
    # Import DBStorage class in this file
    # Create an instance of DBStorage
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    # Import FileStorage class in this file
    # Create an instance of FileStorage
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
