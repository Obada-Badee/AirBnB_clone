#!/usr/bin/python3

"""

This module contains the BaseModel class that
defines all common attributes/methods for other classes

"""

import models
import uuid
from datetime import datetime


class BaseModel:
    """

    A class that defines all common attributes/methods for other classes

    """
    def __init__(self, *args, **kwargs):
        """Initialize an instance of the BaseModel class

        Args:
            args (list): Wont be used yet
            kwargs (dict): This member's arguments will be used
                            for the constructor of a BaseModel
        """

        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs:
            for k, v in kwargs.items():
                if k in ["created_at", "updated_at"]:
                    setattr(self, k, datetime.fromisoformat(v))
                elif k != "__class__":
                    setattr(self, k, v)
        else:
            models.storage.new(self)

    def __str__(self):
        """ A string representation of the class
        Returns:
            The string representation of the class
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """

        Update the public instance attribute `updated_at`
        with the current datetime

        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """ A dictionary representation of the class

        Returns:
        A dictionary containing all keys/values of __dict__
        of the instance.
        a key `__class__` is added to this dictionary with the
        class name of the object.
        `created_at` and `updated_at` must be converted to
        string object in ISO format.

        """

        new_dict = dict(self.__dict__)
        new_dict["__class__"] = self.__class__.__name__
        new_dict["created_at"] = self.created_at.isoformat()
        new_dict["updated_at"] = self.updated_at.isoformat()
        return new_dict
