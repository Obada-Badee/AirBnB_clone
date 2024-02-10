#!/ur/bin/python3

""" A module that defines the Place class"""

from .base_model import BaseModel


class Place(BaseModel):
    """

    The Place class

    Attributes:
        city_id (str): The City's id
        user_id (str): The User's id
        name (str): The Place name
        description(str): The place description
        number_rooms (int): The number of rooms
        number_bathrooms (int): The number of bathrooms
        max_guest (int): The maximum number of guests
        price_by_night (int): The price by night
        latitude (float): The latitude
        longitude (float): The longitude
        amenity_ids (list): The list of Amenity.id

    """
    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
