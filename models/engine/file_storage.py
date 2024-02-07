#!/usr/bin/python3

"""

This module contains the class FileStorage that
serializes instances to a JSON file and
deserializes JSON file to instances

"""

import json
from models.base_model import BaseModel


class FileStorage:
    """

    Serializes instances to a JSON file
    and deserializes JSON file to instances

    Attributes:
        file_path (str): The path to the JSON file
        objects (dict): The dictionary that will store all objects

    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Return the `objects` dict"""
        return FileStorage.__objects

    def new(self, obj):
        """Set in `objects` the `obj` with key <obj class name>.id"""
        FileStorage.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):
        """
        Serialize `objects` class variable
        to the JSON file specified in `file_path` class variable
        """

        with open(FileStorage.__file_path, "w") as f:
            objects_as_dict = {obj_id: obj.to_dict() for obj_id, obj
                               in FileStorage.__objects.items()}
            json.dump(objects_as_dict, f)

    def reload(self):
        """
        Deserialize the JSON file specified in `file_path`
        """

        try:
            with open(FileStorage.__file_path, "r") as f:
                objects_as_dict = json.load(f)
                FileStorage.__objects =
                {obj_id: eval(obj_dict["__class__"])(**obj_dict)
                 for obj_id, obj_dict in objects_as_dict.items()}
        except FileNotFoundError:
            pass
