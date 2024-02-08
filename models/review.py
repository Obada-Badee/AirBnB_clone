#!/usr/bin/python3

""" A module that defines the Review class"""

from .base_model import BaseModel


class Review(BaseModel):
    """

    The Review class

    Attributes:
        place_id (str): The id of the place
        user_id (str): The User's id
        text (str): The review text

    """
    place_id = ""
    user_id = ""
    text = ""
