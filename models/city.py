#!/usr/bin/python3

""" A module that defines the City class"""

from .base_model import BaseModel


class City(BaseModel):
    """

    The City class

    Attributes:
        state_id (str): The id of the State
        name (str): The City's name

    """
    state_id = ""
    name = ""
