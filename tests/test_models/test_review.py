#!/usr/bin/python3

"""Unittest to test the Review class"""

import unittest
import os
from models.review import Review
from models.base_model import BaseModel
from time import sleep
from datetime import datetime
from models import storage


class TestReview_init(unittest.TestCase):
    """Unittest to test the initialization of the Review class"""

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_Review_no_args(self):
        self.assertIs(type(Review()), Review)

    def test_Review_parent(self):
        self.assertIsInstance(Review(), BaseModel)

    def test_Review_default_values(self):
        r = Review()
        self.assertIn(r.id, r.__dict__.values())
        self.assertIn(r.created_at, r.__dict__.values())
        self.assertIn(r.updated_at, r.__dict__.values())

    def test_Review_place_id_is_public(self):
        r = Review()
        self.assertIs(type(Review.place_id), str)
        self.assertIn("place_id", dir(r))
        self.assertNotIn("place_id", r.__dict__)

    def test_Review_user_id_is_public(self):
        r = Review()
        self.assertIs(type(Review.user_id), str)
        self.assertIn("user_id", dir(r))
        self.assertNotIn("user_id", r.__dict__)

    def test_Review_text_is_public(self):
        r = Review()
        self.assertIs(type(Review.text), str)
        self.assertIn("text", dir(r))
        self.assertNotIn("text", r.__dict__)

    def test_Review_value_saved(self):
        self.assertIn(Review(), storage.all().values())

    def test_Review_args_not_used(self):
        r = Review(None)
        self.assertNotIn(None, r.__dict__.values())

    def test_Review_with_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        r = Review(id="12345", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(r, storage.all().values())
        self.assertEqual(r.id, "12345")
        self.assertEqual(r.created_at, dt)
        self.assertEqual(r.updated_at, dt)

    def test_Review_with_args_and_kwargs(self):
        dt = datetime.now()
        iso_dt = dt.isoformat()
        r = Review(None, id="123", created_at=iso_dt, updated_at=iso_dt)
        self.assertNotIn(None, r.__dict__.values())
        self.assertEqual(r.id, "123")
        self.assertEqual(r.created_at, dt)
        self.assertEqual(r.updated_at, dt)

    def test_Review_not_iso_format(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)

    def test_Review_id_type(self):
        self.assertIs(type(Review().id), str)

    def test_Review_unique_id(self):
        r1 = Review()
        r2 = Review()
        self.assertNotEqual(r1.id, r2.id)

    def test_Review_created_at_attr_type(self):
        self.assertIs(type(Review().created_at), datetime)

    def test_Review_updated_at_attr_type(self):
        self.assertIs(type(Review().updated_at), datetime)

    def test_different_created_at_updated_at(self):
        r1 = Review()
        sleep(0.04)
        r2 = Review()
        self.assertLess(r1.created_at, r2.created_at)
        self.assertLess(r1.updated_at, r2.updated_at)

    def test_Review_str_method(self):
        r = Review()
        r.id = '12345'
        r.created_at = r.updated_at = datetime.now()
        dt_repr = repr(r.created_at)
        expected = f"[Review] ({r.id}) {r.__dict__}"
        self.assertIn("'id': '12345'", str(r))
        self.assertIn("'created_at': " + dt_repr, str(r))
        self.assertIn("'updated_at': " + dt_repr, str(r))
        self.assertEqual(expected, str(r))


class TestReview_save(unittest.TestCase):
    """Unittest for the save method of the Review class"""

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
        r = Review()
        old_update_time = r.updated_at
        old_create_time = r.created_at
        sleep(0.04)
        r.save()
        self.assertEqual(r.created_at, old_create_time)
        self.assertGreater(r.updated_at, old_update_time)

    def test_save_two_times(self):
        r = Review()
        old_update_time = r.updated_at
        old_create_time = r.created_at
        sleep(0.04)
        r.save()
        self.assertEqual(r.created_at, old_create_time)
        self.assertGreater(r.updated_at, old_update_time)
        old_update_time = r.updated_at
        sleep(0.04)
        r.save()
        self.assertGreater(r.updated_at, old_update_time)

    def test_save_to_json(self):
        r = Review()
        r.save()
        with open("file.json", "r", encoding="UTF8") as f:
            self.assertIn(f"Review.{r.id}", f.read())

    def test_save_time_with_args(self):
        with self.assertRaises(TypeError):
            Review().save("invalid arg")


class TestReview_to_dict(unittest.TestCase):
    """Unittest for the to_dict method of the Review class"""

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

    def test_Review_to_dict_type(self):
        r = Review()
        self.assertIs(type(r.to_dict()), dict)

    def test_Review_to_dict_keys(self):
        r = Review()
        self.assertIn("__class__", r.to_dict())
        self.assertIn("id", r.to_dict())
        self.assertIn("created_at", r.to_dict())
        self.assertIn("updated_at", r.to_dict())

    def test_Review_additional_to_dict_attributes(self):
        r = Review()
        self.assertEqual("Review", r.to_dict()["__class__"])
        self.assertIsNot(r.created_at, r.to_dict()["created_at"])
        self.assertIsNot(r.updated_at, r.to_dict()["updated_at"])
        self.assertIs(type(r.to_dict()["created_at"]), str)
        self.assertIs(type(r.to_dict()["updated_at"]), str)

    def test_Review_add_attribute_to_dict(self):
        r = Review()
        r.name = "Mohammed"
        self.assertIn("name", r.to_dict().keys())

    def test_Review_to_dict_output(self):
        r = Review()
        expected = {
                'id': r.id,
                '__class__': 'Review',
                'created_at': r.created_at.isoformat(),
                'updated_at': r.updated_at.isoformat()
                }
        self.assertEqual(r.to_dict(), expected)

    def test_Review_to_dict_differences(self):
        r = Review()
        self.assertNotEqual(r.to_dict(), r.__dict__)

    def test_Review_to_dict_with_args(self):
        with self.assertRaises(TypeError):
            Review().to_dict("Invalid")


if __name__ == "__main__":
    unittest.main()
