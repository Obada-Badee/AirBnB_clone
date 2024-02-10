#!/usr/bin/python3

"""Unittest to test the State class"""

import unittest
import os
from models.state import State
from models.base_model import BaseModel
from time import sleep
from datetime import datetime
from models import storage


class TestState_init(unittest.TestCase):
    """Unittest to test the initialization of the State class"""

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_State_no_args(self):
        self.assertIs(type(State()), State)

    def test_State_parent(self):
        self.assertIsInstance(State(), BaseModel)

    def test_State_default_values(self):
        s = State()
        self.assertIn(s.id, s.__dict__.values())
        self.assertIn(s.created_at, s.__dict__.values())
        self.assertIn(s.updated_at, s.__dict__.values())

    def test_State_name_is_public(self):
        s = State()
        self.assertIs(type(State.name), str)
        self.assertIn("name", dir(s))
        self.assertNotIn("name", s.__dict__)

    def test_State_value_saved(self):
        self.assertIn(State(), storage.all().values())

    def test_State_args_not_used(self):
        s = State(None)
        self.assertNotIn(None, s.__dict__.values())

    def test_State_with_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        s = State(id="12345", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(s, storage.all().values())
        self.assertEqual(s.id, "12345")
        self.assertEqual(s.created_at, dt)
        self.assertEqual(s.updated_at, dt)

    def test_State_with_args_and_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        s = State(None, id="123", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(None, s.__dict__.values())
        self.assertEqual(s.id, "123")
        self.assertEqual(s.created_at, dt)
        self.assertEqual(s.updated_at, dt)

    def test_State_not_iso_format(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)

    def test_State_id_type(self):
        self.assertIs(type(State().id), str)

    def test_State_unique_id(self):
        s1 = State()
        s2 = State()
        self.assertNotEqual(s1.id, s2.id)

    def test_State_created_at_attr_type(self):
        self.assertIs(type(State().created_at), datetime)

    def test_State_updated_at_attr_type(self):
        self.assertIs(type(State().updated_at), datetime)

    def test_different_created_at_updated_at(self):
        s1 = State()
        sleep(0.04)
        s2 = State()
        self.assertLess(s1.created_at, s2.created_at)
        self.assertLess(s1.updated_at, s2.updated_at)

    def test_State_str_method(self):
        s = State()
        s.id = '12345'
        s.created_at = s.updated_at = datetime.now()
        dt_repr = repr(s.created_at)
        expected = f"[State] ({s.id}) {s.__dict__}"
        self.assertIn("'id': '12345'", str(s))
        self.assertIn("'created_at': " + dt_repr, str(s))
        self.assertIn("'updated_at': " + dt_repr, str(s))
        self.assertEqual(expected, str(s))


class TestState_save(unittest.TestCase):
    """Unittest for the save method of the State class"""

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
        s = State()
        old_update_time = s.updated_at
        old_create_time = s.created_at
        sleep(0.04)
        s.save()
        self.assertEqual(s.created_at, old_create_time)
        self.assertGreater(s.updated_at, old_update_time)

    def test_save_two_times(self):
        s = State()
        old_update_time = s.updated_at
        old_create_time = s.created_at
        sleep(0.04)
        s.save()
        self.assertEqual(s.created_at, old_create_time)
        self.assertGreater(s.updated_at, old_update_time)
        old_update_time = s.updated_at
        sleep(0.04)
        s.save()
        self.assertGreater(s.updated_at, old_update_time)

    def test_save_to_json(self):
        s = State()
        s.save()
        with open("file.json", "r", encoding="UTF8") as f:
            self.assertIn(f"State.{s.id}", f.read())

    def test_save_time_with_args(self):
        with self.assertRaises(TypeError):
            State().save("invalid arg")


class TestState_to_dict(unittest.TestCase):
    """Unittest for the to_dict method of the State class"""

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

    def test_State_to_dict_type(self):
        s = State()
        self.assertIs(type(s.to_dict()), dict)

    def test_State_to_dict_keys(self):
        s = State()
        self.assertIn("__class__", s.to_dict())
        self.assertIn("id", s.to_dict())
        self.assertIn("created_at", s.to_dict())
        self.assertIn("updated_at", s.to_dict())

    def test_State_additional_to_dict_attributes_type(self):
        s = State()
        self.assertEqual("State", s.to_dict()["__class__"])
        self.assertIsNot(s.created_at, s.to_dict()["created_at"])
        self.assertIsNot(s.updated_at, s.to_dict()["updated_at"])
        self.assertIs(type(s.to_dict()["created_at"]), str)
        self.assertIs(type(s.to_dict()["updated_at"]), str)

    def test_State_add_attribute_to_dict(self):
        s = State()
        s.name = "Mohammed"
        self.assertIn("name", s.to_dict().keys())

    def test_State_to_dict_output(self):
        s = State()
        expected = {
                'id': s.id,
                '__class__': 'State',
                'created_at': s.created_at.isoformat(),
                'updated_at': s.updated_at.isoformat()
                }
        self.assertEqual(s.to_dict(), expected)

    def test_State_to_dict_differences(self):
        s = State()
        self.assertNotEqual(s.to_dict(), s.__dict__)

    def test_State_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            State().to_dict("Invalid")


if __name__ == "__main__":
    unittest.main()
