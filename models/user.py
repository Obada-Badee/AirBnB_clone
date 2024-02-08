#!/usr/bin/python3

""" A module that defines the user class"""

from .base_model import BaseModel


class User(BaseModel):
    """

    The user class

    Attributes:
        email (str): The user's email
        password (str): The user's password
        first_name (str): The user's first_name
        last_name (str): The user's last_name

    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
