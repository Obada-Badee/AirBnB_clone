#!/usr/bin/python3

"""Unittest to test the Amenity class"""

import unittest
import os
from models.amenity import Amenity
from models.base_model import BaseModel
from time import sleep
from datetime import datetime
from models import storage


class TestAmenity_init(unittest.TestCase):
    """Unittest to test the initialization of the Amenity class"""

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_Amenity_no_args(self):
        self.assertIs(type(Amenity()), Amenity)

    def test_Amenity_parent(self):
        self.assertIsInstance(Amenity(), BaseModel)

    def test_Amenity_default_values(self):
        a = Amenity()
        self.assertIn(a.id, a.__dict__.values())
        self.assertIn(a.created_at, a.__dict__.values())
        self.assertIn(a.updated_at, a.__dict__.values())

    def test_Amenity_name_is_public(self):
        a = Amenity()
        self.assertIs(type(Amenity.name), str)
        self.assertIn("name", dir(a))
        self.assertNotIn("name", a.__dict__)

    def test_Amenity_value_saved(self):
        self.assertIn(Amenity(), storage.all().values())

    def test_Amenity_args_not_used(self):
        a = Amenity(None)
        self.assertNotIn(None, a.__dict__.values())

    def test_Amenity_with_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        a = Amenity(id="12345", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(a, storage.all().values())
        self.assertEqual(a.id, "12345")
        self.assertEqual(a.created_at, dt)
        self.assertEqual(a.updated_at, dt)

    def test_Amenity_with_args_and_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        a = Amenity(None, id="123", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(None, a.__dict__.values())
        self.assertEqual(a.id, "123")
        self.assertEqual(a.created_at, dt)
        self.assertEqual(a.updated_at, dt)

    def test_Amenity_not_iso_format(self):
        with self.assertRaises(TypeError):
            Amenity(id=None, created_at=None, updated_at=None)

    def test_Amenity_id_type(self):
        self.assertIs(type(Amenity().id), str)

    def test_Amenity_unique_id(self):
        a1 = Amenity()
        a2 = Amenity()
        self.assertNotEqual(a1.id, a2.id)

    def test_Amenity_created_at_attr_type(self):
        self.assertIs(type(Amenity().created_at), datetime)

    def test_Amenity_updated_at_attr_type(self):
        self.assertIs(type(Amenity().updated_at), datetime)

    def test_different_created_at_updated_at(self):
        a1 = Amenity()
        sleep(0.04)
        a2 = Amenity()
        self.assertLess(a1.created_at, a2.created_at)
        self.assertLess(a1.updated_at, a2.updated_at)

    def test_Amenity_str_method(self):
        a = Amenity()
        a.id = '12345'
        a.created_at = a.updated_at = datetime.now()
        dt_repr = repr(a.created_at)
        expected = f"[Amenity] ({a.id}) {a.__dict__}"
        self.assertIn("'id': '12345'", str(a))
        self.assertIn("'created_at': " + dt_repr, str(a))
        self.assertIn("'updated_at': " + dt_repr, str(a))
        self.assertEqual(expected, str(a))


class TestAmenity_save(unittest.TestCase):
    """Unittest for the save method of the Amenity class"""

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
        a = Amenity()
        old_update_time = a.updated_at
        old_create_time = a.created_at
        sleep(0.04)
        a.save()
        self.assertEqual(a.created_at, old_create_time)
        self.assertGreater(a.updated_at, old_update_time)

    def test_save_two_times(self):
        a = Amenity()
        old_update_time = a.updated_at
        old_create_time = a.created_at
        sleep(0.04)
        a.save()
        self.assertEqual(a.created_at, old_create_time)
        self.assertGreater(a.updated_at, old_update_time)
        old_update_time = a.updated_at
        sleep(0.04)
        a.save()
        self.assertGreater(a.updated_at, old_update_time)

    def test_save_to_json(self):
        a = Amenity()
        a.save()
        with open("file.json", "r", encoding="UTF8") as f:
            self.assertIn(f"Amenity.{a.id}", f.read())

    def test_save_time_with_args(self):
        with self.assertRaises(TypeError):
            Amenity().save("invalid arg")


class TestAmenity_to_dict(unittest.TestCase):
    """Unittest for the to_dict method of the Amenity class"""

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

    def test_Amenity_to_dict_type(self):
        a = Amenity()
        self.assertIs(type(a.to_dict()), dict)

    def test_Amenity_to_dict_keys(self):
        a = Amenity()
        self.assertIn("__class__", a.to_dict())
        self.assertIn("id", a.to_dict())
        self.assertIn("created_at", a.to_dict())
        self.assertIn("updated_at", a.to_dict())

    def test_Amenity_additional_to_dict_attributes(self):
        a = Amenity()
        self.assertEqual("Amenity", a.to_dict()["__class__"])
        self.assertIsNot(a.created_at, a.to_dict()["created_at"])
        self.assertIsNot(a.updated_at, a.to_dict()["updated_at"])
        self.assertIs(type(a.to_dict()["created_at"]), str)
        self.assertIs(type(a.to_dict()["updated_at"]), str)

    def test_Amenity_add_attribute_to_dict(self):
        a = Amenity()
        a.name = "Mohammed"
        self.assertIn("name", a.to_dict().keys())

    def test_Amenity_to_dict_output(self):
        a = Amenity()
        expected = {
                'id': a.id,
                '__class__': 'Amenity',
                'created_at': a.created_at.isoformat(),
                'updated_at': a.updated_at.isoformat()
                }
        self.assertEqual(a.to_dict(), expected)

    def test_Amenity_to_dict_differences(self):
        a = Amenity()
        self.assertNotEqual(a.to_dict(), a.__dict__)

    def test_Amenity_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            Amenity().to_dict("Invalid")


if __name__ == "__main__":
    unittest.main()
