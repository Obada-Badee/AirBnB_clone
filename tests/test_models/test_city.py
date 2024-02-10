#!/usr/bin/python3

"""Unittest to test the City class"""

import unittest
import os
from models.city import City
from models.base_model import BaseModel
from time import sleep
from datetime import datetime
from models import storage


class TestCity_init(unittest.TestCase):
    """Unittest to test the initialization of the City class"""

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_City_no_args(self):
        self.assertIs(type(City()), City)

    def test_City_parent(self):
        self.assertIsInstance(City(), BaseModel)

    def test_City_default_values(self):
        c = City()
        self.assertIn(c.id, c.__dict__.values())
        self.assertIn(c.created_at, c.__dict__.values())
        self.assertIn(c.updated_at, c.__dict__.values())

    def test_User_state_id_is_public(self):
        c = City()
        self.assertIs(type(City.state_id), str)
        self.assertIn("state_id", dir(c))
        self.assertNotIn("state_id", c.__dict__)

    def test_User_name_is_public(self):
        c = City()
        self.assertIs(type(City.name), str)
        self.assertIn("name", dir(c))
        self.assertNotIn("name", c.__dict__)

    def test_City_value_saved(self):
        self.assertIn(City(), storage.all().values())

    def test_City_args_not_used(self):
        c = City(None)
        self.assertNotIn(None, c.__dict__.values())

    def test_City_with_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        c = City(id="12345", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(c, storage.all().values())
        self.assertEqual(c.id, "12345")
        self.assertEqual(c.created_at, dt)
        self.assertEqual(c.updated_at, dt)

    def test_City_with_args_and_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        c = City(None, id="123", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(None, c.__dict__.values())
        self.assertEqual(c.id, "123")
        self.assertEqual(c.created_at, dt)
        self.assertEqual(c.updated_at, dt)

    def test_City_not_iso_format(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)

    def test_City_id_type(self):
        self.assertIs(type(City().id), str)

    def test_City_unique_id(self):
        c1 = City()
        c2 = City()
        self.assertNotEqual(c1.id, c2.id)

    def test_City_created_at_attr_type(self):
        self.assertIs(type(City().created_at), datetime)

    def test_City_updated_at_attr_type(self):
        self.assertIs(type(City().updated_at), datetime)

    def test_different_created_at_updated_at(self):
        c1 = City()
        sleep(0.04)
        c2 = City()
        self.assertLess(c1.created_at, c2.created_at)
        self.assertLess(c1.updated_at, c2.updated_at)

    def test_City_str_method(self):
        c = City()
        c.id = '12345'
        c.created_at = c.updated_at = datetime.now()
        dt_repr = repr(c.created_at)
        expected = f"[City] ({c.id}) {c.__dict__}"
        self.assertIn("'id': '12345'", str(c))
        self.assertIn("'created_at': " + dt_repr, str(c))
        self.assertIn("'updated_at': " + dt_repr, str(c))
        self.assertEqual(expected, str(c))


class TestCity_save(unittest.TestCase):
    """Unittest for the save method of the City class"""

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
        c = City()
        old_update_time = c.updated_at
        old_create_time = c.created_at
        sleep(0.04)
        c.save()
        self.assertEqual(c.created_at, old_create_time)
        self.assertGreater(c.updated_at, old_update_time)

    def test_save_two_times(self):
        c = City()
        old_update_time = c.updated_at
        old_create_time = c.created_at
        sleep(0.04)
        c.save()
        self.assertEqual(c.created_at, old_create_time)
        self.assertGreater(c.updated_at, old_update_time)
        old_update_time = c.updated_at
        sleep(0.04)
        c.save()
        self.assertGreater(c.updated_at, old_update_time)

    def test_save_to_json(self):
        c = City()
        c.save()
        with open("file.json", "r", encoding="UTF8") as f:
            self.assertIn(f"City.{c.id}", f.read())

    def test_save_time_with_args(self):
        with self.assertRaises(TypeError):
            City().save("invalid arg")


class TestCity_to_dict(unittest.TestCase):
    """Unittest for the to_dict method of the City class"""

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

    def test_City_to_dict_type(self):
        c = City()
        self.assertIs(type(c.to_dict()), dict)

    def test_City_to_dict_keys(self):
        c = City()
        self.assertIn("__class__", c.to_dict())
        self.assertIn("id", c.to_dict())
        self.assertIn("created_at", c.to_dict())
        self.assertIn("updated_at", c.to_dict())

    def test_City_additional_to_dict_attributes(self):
        c = City()
        self.assertEqual("City", c.to_dict()["__class__"])
        self.assertIsNot(c.created_at, c.to_dict()["created_at"])
        self.assertIsNot(c.updated_at, c.to_dict()["updated_at"])
        self.assertIs(type(c.to_dict()["created_at"]), str)
        self.assertIs(type(c.to_dict()["updated_at"]), str)

    def test_City_add_attribute_to_dict(self):
        c = City()
        c.name = "Mohammed"
        self.assertIn("name", c.to_dict().keys())

    def test_City_to_dict_output(self):
        c = City()
        expected = {
                'id': c.id,
                '__class__': 'City',
                'created_at': c.created_at.isoformat(),
                'updated_at': c.updated_at.isoformat()
                }
        self.assertEqual(c.to_dict(), expected)

    def test_City_to_dict_differences(self):
        c = City()
        self.assertNotEqual(c.to_dict(), c.__dict__)

    def test_City_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            City().to_dict("Invalid")


if __name__ == "__main__":
    unittest.main()
