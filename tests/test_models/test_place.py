#!/usr/bin/python3

"""Unittest to test the Place class"""

import unittest
import os
from models.place import Place
from models.base_model import BaseModel
from time import sleep
from datetime import datetime
from models import storage


class TestPlace_init(unittest.TestCase):
    """Unittest to test the initialization of the Place class"""

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_Place_no_args(self):
        self.assertIs(type(Place()), Place)

    def test_Place_parent(self):
        self.assertIsInstance(Place(), BaseModel)

    def test_Place_default_values(self):
        p = Place()
        self.assertIn(p.id, p.__dict__.values())
        self.assertIn(p.created_at, p.__dict__.values())
        self.assertIn(p.updated_at, p.__dict__.values())

    def test_Place_name_is_public(self):
        p = Place()
        self.assertIs(type(Place.name), str)
        self.assertIn("name", dir(p))
        self.assertNotIn("name", p.__dict__)

    def test_Place_city_id_is_public(self):
        p = Place()
        self.assertIs(type(Place.city_id), str)
        self.assertIn("city_id", dir(p))
        self.assertNotIn("city_id", p.__dict__)

    def test_Place_user_id_is_public(self):
        p = Place()
        self.assertIs(type(Place.user_id), str)
        self.assertIn("user_id", dir(p))
        self.assertNotIn("user_id", p.__dict__)

    def test_Place_description_is_public(self):
        p = Place()
        self.assertIs(type(Place.description), str)
        self.assertIn("description", dir(p))
        self.assertNotIn("description", p.__dict__)

    def test_Place_number_rooms_is_public(self):
        p = Place()
        self.assertIs(type(Place.number_rooms), int)
        self.assertIn("number_rooms", dir(p))
        self.assertNotIn("number_rooms", p.__dict__)

    def test_Place_number_bathrooms_is_public(self):
        p = Place()
        self.assertIs(type(Place.number_bathrooms), int)
        self.assertIn("number_bathrooms", dir(p))
        self.assertNotIn("number_bathrooms", p.__dict__)

    def test_Place_max_guest_is_public(self):
        p = Place()
        self.assertIs(type(Place.max_guest), int)
        self.assertIn("max_guest", dir(p))
        self.assertNotIn("max_guest", p.__dict__)

    def test_Place_price_by_night_is_public(self):
        p = Place()
        self.assertIs(type(Place.price_by_night), int)
        self.assertIn("price_by_night", dir(p))
        self.assertNotIn("price_by_night", p.__dict__)

    def test_Place_latitude_is_public(self):
        p = Place()
        self.assertIs(type(Place.latitude), float)
        self.assertIn("latitude", dir(p))
        self.assertNotIn("latitude", p.__dict__)

    def test_Place_longitude_is_public(self):
        p = Place()
        self.assertIs(type(Place.longitude), float)
        self.assertIn("longitude", dir(p))
        self.assertNotIn("longitude", p.__dict__)

    def test_Place_amenity_ids_is_public(self):
        p = Place()
        self.assertIs(type(Place.amenity_ids), list)
        self.assertIn("amenity_ids", dir(p))
        self.assertNotIn("amenity_ids", p.__dict__)

    def test_Place_value_saved(self):
        self.assertIn(Place(), storage.all().values())

    def test_Place_args_not_used(self):
        p = Place(None)
        self.assertNotIn(None, p.__dict__.values())

    def test_Place_with_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        p = Place(id="12345", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(p, storage.all().values())
        self.assertEqual(p.id, "12345")
        self.assertEqual(p.created_at, dt)
        self.assertEqual(p.updated_at, dt)

    def test_Place_with_args_and_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        p = Place(None, id="123", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(None, p.__dict__.values())
        self.assertEqual(p.id, "123")
        self.assertEqual(p.created_at, dt)
        self.assertEqual(p.updated_at, dt)

    def test_Place_not_iso_format(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)

    def test_Place_id_type(self):
        self.assertIs(type(Place().id), str)

    def test_Place_unique_id(self):
        p1 = Place()
        p2 = Place()
        self.assertNotEqual(p1.id, p2.id)

    def test_Place_created_at_attr_type(self):
        self.assertIs(type(Place().created_at), datetime)

    def test_Place_updated_at_attr_type(self):
        self.assertIs(type(Place().updated_at), datetime)

    def test_different_created_at_updated_at(self):
        p1 = Place()
        sleep(0.04)
        p2 = Place()
        self.assertLess(p1.created_at, p2.created_at)
        self.assertLess(p1.updated_at, p2.updated_at)

    def test_Place_str_method(self):
        p = Place()
        p.id = '12345'
        p.created_at = p.updated_at = datetime.now()
        dt_repr = repr(p.created_at)
        expected = f"[Place] ({p.id}) {p.__dict__}"
        self.assertIn("'id': '12345'", str(p))
        self.assertIn("'created_at': " + dt_repr, str(p))
        self.assertIn("'updated_at': " + dt_repr, str(p))
        self.assertEqual(expected, str(p))


class TestPlace_save(unittest.TestCase):
    """Unittest for the save method of the Place class"""

    def setUp(self):
        try:
            os.rename("tmp.json", "file.json")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_save_time_updated(self):
        p = Place()
        old_update_time = p.updated_at
        old_create_time = p.created_at
        sleep(0.04)
        p.save()
        self.assertEqual(p.created_at, old_create_time)
        self.assertGreater(p.updated_at, old_update_time)

    def test_save_two_times(self):
        p = Place()
        old_update_time = p.updated_at
        old_create_time = p.created_at
        sleep(0.04)
        p.save()
        self.assertEqual(p.created_at, old_create_time)
        self.assertGreater(p.updated_at, old_update_time)
        old_update_time = p.updated_at
        sleep(0.04)
        p.save()
        self.assertGreater(p.updated_at, old_update_time)

    def test_save_to_json(self):
        p = Place()
        p.save()
        with open("file.json", "r", encoding="UTF8") as f:
            self.assertIn(f"Place.{p.id}", f.read())

    def test_save_time_with_args(self):
        with self.assertRaises(TypeError):
            Place().save("invalid arg")


class TestPlace_to_dict(unittest.TestCase):
    """Unittest for the to_dict method of the Place class"""

    def setUp(self):
        try:
            os.rename("tmp.json", "file.json")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp.json", "file.json")
        except IOError:
            pass

    def test_Place_to_dict_type(self):
        p = Place()
        self.assertIs(type(p.to_dict()), dict)

    def test_Place_to_dict_keys(self):
        p = Place()
        self.assertIn("__class__", p.to_dict())
        self.assertIn("id", p.to_dict())
        self.assertIn("created_at", p.to_dict())
        self.assertIn("updated_at", p.to_dict())

    def test_Place_additional_to_dict_attributes(self):
        p = Place()
        self.assertEqual("Place", p.to_dict()["__class__"])
        self.assertIsNot(p.created_at, p.to_dict()["created_at"])
        self.assertIsNot(p.updated_at, p.to_dict()["updated_at"])
        self.assertIs(type(p.to_dict()["created_at"]), str)
        self.assertIs(type(p.to_dict()["updated_at"]), str)

    def test_Place_add_attribute_to_dict(self):
        p = Place()
        p.name = "Mohammed"
        self.assertIn("name", p.to_dict().keys())

    def test_Place_to_dict_output(self):
        p = Place()
        expected = {
                'id': p.id,
                '__class__': 'Place',
                'created_at': p.created_at.isoformat(),
                'updated_at': p.updated_at.isoformat()
                }
        self.assertEqual(p.to_dict(), expected)

    def test_Place_to_dict_differences(self):
        p = Place()
        self.assertNotEqual(p.to_dict(), p.__dict__)

    def test_Place_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            Place().to_dict("Invalid")


if __name__ == "__main__":
    unittest.main()
