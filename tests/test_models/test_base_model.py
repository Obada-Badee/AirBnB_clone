#!/usr/bin/python3

""" Unittest to test the BaseModel class"""

import unittest
import os
from time import sleep
from datetime import datetime
from models.base_model import BaseModel
from models import storage


class TestBaseModel_Init(unittest.TestCase):
    """ Test the initialization of the BaseModel"""

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_BaseModel_no_args(self):
        self.assertIs(type(BaseModel()), BaseModel)

    def test_BaseModel_value_saved(self):
        self.assertIn(BaseModel(), storage.all().values())

    def test_BaseModel_args_not_used(self):
        b = BaseModel(None)
        self.assertNotIn(None, b.__dict__.values())

    def test_BaseModel_with_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        b = BaseModel(id="12345", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(b, storage.all().values())
        self.assertEqual(b.id, "12345")
        self.assertEqual(b.created_at, dt)
        self.assertEqual(b.updated_at, dt)

    def test_BaseModel_with_args_and_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        b = BaseModel(None, id="123", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(None, b.__dict__.values())
        self.assertEqual(b.id, "123")
        self.assertEqual(b.created_at, dt)
        self.assertEqual(b.updated_at, dt)

    def test_BaseModel_not_iso_format(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_BaseModel_id_type(self):
        self.assertIs(type(BaseModel().id), str)

    def test_BaseModel_unique_id(self):
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertNotEqual(b1.id, b2.id)

    def test_BaseModel_created_at_attr_type(self):
        self.assertIs(type(BaseModel().created_at), datetime)

    def test_BaseModel_updated_at_attr_type(self):
        self.assertIs(type(BaseModel().updated_at), datetime)

    def test_different_created_at(self):
        b1 = BaseModel()
        sleep(0.04)
        b2 = BaseModel()
        self.assertLess(b1.created_at, b2.created_at)

    def test_different_updated_at(self):
        b1 = BaseModel()
        sleep(0.04)
        b2 = BaseModel()
        self.assertLess(b1.updated_at, b2.updated_at)

    def test_BaseModel_str_method(self):
        b = BaseModel()
        b.id = '12345'
        b.created_at = b.updated_at = datetime.now()
        dt_repr = repr(b.created_at)
        expected = f"[BaseModel] ({b.id}) {b.__dict__}"
        self.assertIn("'id': '12345'", str(b))
        self.assertIn("'created_at': " + dt_repr, str(b))
        self.assertIn("'updated_at': " + dt_repr, str(b))
        self.assertEqual(expected, str(b))


class TestBaseModel_save(unittest.TestCase):
    """Unittest for the save method of the BaseModel class"""

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

    def test_save_time_updated(self):
        b = BaseModel()
        old_update_time = b.updated_at
        old_create_time = b.created_at
        sleep(0.04)
        b.save()
        self.assertEqual(b.created_at, old_create_time)
        self.assertGreater(b.updated_at, old_update_time)

    def test_save_two_times(self):
        b = BaseModel()
        old_update_time = b.updated_at
        old_create_time = b.created_at
        sleep(0.04)
        b.save()
        self.assertEqual(b.created_at, old_create_time)
        self.assertGreater(b.updated_at, old_update_time)
        old_update_time = b.updated_at
        sleep(0.04)
        b.save()
        self.assertGreater(b.updated_at, old_update_time)

    def test_save_to_json(self):
        b = BaseModel()
        b.save()
        with open("file.json", "r", encoding="UTF8") as f:
            self.assertIn(f"BaseModel.{b.id}", f.read())

    def test_save_time_with_args(self):
        with self.assertRaises(TypeError):
            BaseModel().save("invalid arg")


class TestBaseModel_to_dict(unittest.TestCase):
    """Unittest for the to_dict method of the BaseModel class"""

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

    def test_BaseModel_to_dict_type(self):
        b = BaseModel()
        self.assertIs(type(b.to_dict()), dict)

    def test_BaseModel_to_dict_keys(self):
        b = BaseModel()
        self.assertIn("__class__", b.to_dict())
        self.assertIn("id", b.to_dict())
        self.assertIn("created_at", b.to_dict())
        self.assertIn("updated_at", b.to_dict())

    def test_BaseModel_additional_to_dict_attributes_type(self):
        b = BaseModel()
        self.assertEqual("BaseModel", b.to_dict()["__class__"])
        self.assertIsNot(b.created_at, b.to_dict()["created_at"])
        self.assertIsNot(b.updated_at, b.to_dict()["updated_at"])
        self.assertIs(type(b.to_dict()["created_at"]), str)
        self.assertIs(type(b.to_dict()["updated_at"]), str)

    def test_BaseModel_add_attribute_to_dict(self):
        b = BaseModel()
        b.name = "Mohammed"
        self.assertIn("name", b.to_dict().keys())

    def test_BaseModel_to_dict_output(self):
        b = BaseModel()
        expected = {
                'id': b.id,
                '__class__': 'BaseModel',
                'created_at': b.created_at.isoformat(),
                'updated_at': b.updated_at.isoformat()
                }
        self.assertEqual(b.to_dict(), expected)

    def test_BaseModel_to_dict_differences(self):
        b = BaseModel()
        self.assertNotEqual(b.to_dict(), b.__dict__)

    def test_BaseModel_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            BaseModel().to_dict("Invalid")


if __name__ == "__main__":
    unittest.main()
