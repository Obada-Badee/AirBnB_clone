#!/usr/bin/python3

"""Unittest to test the User class"""

import unittest
import os
from models.user import User
from models.base_model import BaseModel
from time import sleep
from datetime import datetime
from models import storage


class TestUser_init(unittest.TestCase):
    """Unittest to test the initialization of the User class"""

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_User_no_args(self):
        self.assertIs(type(User()), User)

    def test_User_parent(self):
        self.assertIsInstance(User(), BaseModel)

    def test_User_default_values(self):
        u = User()
        self.assertIn(u.id, u.__dict__.values())
        self.assertIn(u.created_at, u.__dict__.values())
        self.assertIn(u.updated_at, u.__dict__.values())

    def test_User_email_is_public(self):
        u = User()
        self.assertIs(type(User.email), str)
        self.assertIn("email", dir(u))
        self.assertNotIn("email", u.__dict__)

    def test_User_passowrd_is_public(self):
        u = User()
        self.assertIs(type(User.password), str)
        self.assertIn("password", dir(u))
        self.assertNotIn("password", u.__dict__)

    def test_User_first_name_is_public(self):
        u = User()
        self.assertIs(type(User.first_name), str)
        self.assertIn("first_name", dir(u))
        self.assertNotIn("first_name", u.__dict__)

    def test_User_last_name_is_public(self):
        u = User()
        self.assertIs(type(User.last_name), str)
        self.assertIn("last_name", dir(u))
        self.assertNotIn("last_name", u.__dict__)

    def test_User_value_saved(self):
        self.assertIn(User(), storage.all().values())

    def test_User_args_not_used(self):
        u = User(None)
        self.assertNotIn(None, u.__dict__.values())

    def test_User_with_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        u = User(id="12345", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(u, storage.all().values())
        self.assertEqual(u.id, "12345")
        self.assertEqual(u.created_at, dt)
        self.assertEqual(u.updated_at, dt)

    def test_User_with_args_and_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        u = User(None, id="123", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(None, u.__dict__.values())
        self.assertEqual(u.id, "123")
        self.assertEqual(u.created_at, dt)
        self.assertEqual(u.updated_at, dt)

    def test_User_not_iso_format(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)

    def test_User_id_type(self):
        self.assertIs(type(User().id), str)

    def test_User_unique_id(self):
        u1 = User()
        u2 = User()
        self.assertNotEqual(u1.id, u2.id)

    def test_User_created_at_attr_type(self):
        self.assertIs(type(User().created_at), datetime)

    def test_User_updated_at_attr_type(self):
        self.assertIs(type(User().updated_at), datetime)

    def test_different_created_at_updated_at(self):
        u1 = User()
        sleep(0.04)
        u2 = User()
        self.assertLess(u1.created_at, u2.created_at)
        self.assertLess(u1.updated_at, u2.updated_at)

    def test_User_str_method(self):
        u = User()
        u.id = '12345'
        u.created_at = u.updated_at = datetime.now()
        dt_repr = repr(u.created_at)
        expected = f"[User] ({u.id}) {u.__dict__}"
        self.assertIn("'id': '12345'", str(u))
        self.assertIn("'created_at': " + dt_repr, str(u))
        self.assertIn("'updated_at': " + dt_repr, str(u))
        self.assertEqual(expected, str(u))


class TestUser_save(unittest.TestCase):
    """Unittest for the save method of the User class"""

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
        u = User()
        old_update_time = u.updated_at
        old_create_time = u.created_at
        sleep(0.04)
        u.save()
        self.assertEqual(u.created_at, old_create_time)
        self.assertGreater(u.updated_at, old_update_time)

    def test_save_two_times(self):
        u = User()
        old_update_time = u.updated_at
        old_create_time = u.created_at
        sleep(0.04)
        u.save()
        self.assertEqual(u.created_at, old_create_time)
        self.assertGreater(u.updated_at, old_update_time)
        old_update_time = u.updated_at
        sleep(0.04)
        u.save()
        self.assertGreater(u.updated_at, old_update_time)

    def test_save_to_json(self):
        u = User()
        u.save()
        with open("file.json", "r", encoding="UTF8") as f:
            self.assertIn(f"User.{u.id}", f.read())

    def test_save_time_with_args(self):
        with self.assertRaises(TypeError):
            User().save("invalid arg")


class TestUser_to_dict(unittest.TestCase):
    """Unittest for the to_dict method of the User class"""

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

    def test_User_to_dict_type(self):
        u = User()
        self.assertIs(type(u.to_dict()), dict)

    def test_User_to_dict_keys(self):
        u = User()
        self.assertIn("__class__", u.to_dict())
        self.assertIn("id", u.to_dict())
        self.assertIn("created_at", u.to_dict())
        self.assertIn("updated_at", u.to_dict())

    def test_User_additional_to_dict_attributes_type(self):
        u = User()
        self.assertEqual("User", u.to_dict()["__class__"])
        self.assertIsNot(u.created_at, u.to_dict()["created_at"])
        self.assertIsNot(u.updated_at, u.to_dict()["updated_at"])
        self.assertIs(type(u.to_dict()["created_at"]), str)
        self.assertIs(type(u.to_dict()["updated_at"]), str)

    def test_User_add_attribute_to_dict(self):
        u = User()
        u.name = "Mohammed"
        self.assertIn("name", u.to_dict().keys())

    def test_User_to_dict_output(self):
        u = User()
        expected = {
                'id': u.id,
                '__class__': 'User',
                'created_at': u.created_at.isoformat(),
                'updated_at': u.updated_at.isoformat()
                }
        self.assertEqual(u.to_dict(), expected)

    def test_User_to_dict_differences(self):
        u = User()
        self.assertNotEqual(u.to_dict(), u.__dict__)

    def test_User_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            User().to_dict("Invalid")


if __name__ == "__main__":
    unittest.main()
