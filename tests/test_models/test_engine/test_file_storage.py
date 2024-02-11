#!/usr/bin/python3

"""Unittest to test the FileStorage class"""

import unittest
import models
import os
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class TestFileStorage_init(unittest.TestCase):
    """Test the initializtion of the file storage class"""

    def setUp(self):
        try:
            os.rename("file.json", "tmp.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmp.json", "file.json")
        except FileNotFoundError:
            pass

    def test_init_no_args(self):
        self.assertIs(type(FileStorage()), FileStorage)

    def test_init_private_attributes(self):
        fs = FileStorage()
        self.assertIs(type(fs._FileStorage__file_path), str)
        self.assertIs(type(fs._FileStorage__objects), dict)

    def test_init_one_arg(self):
        with self.assertRaises(TypeError):
            FileStorage("Invalid way")

    def test_storage_init(self):
        self.assertIs(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """Test the methods of the FileStorage class"""

    def setUp(self):
        try:
            os.rename("file.json", "tmp.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmp.json", "file.json")
        except FileNotFoundError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all_no_args(self):
        self.assertIs(type(models.storage.all()), dict)

    def test_all_one_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all("Invalid way")

    def test_new_no_args(self):
        with self.assertRaises(TypeError):
            models.storage.new()

    def test_new_one_arg(self):
        b = BaseModel()
        u = User()
        s = State()
        c = City()
        a = Amenity()
        p = Place()
        r = Review()

        models.storage.new(b)
        models.storage.new(u)
        models.storage.new(s)
        models.storage.new(c)
        models.storage.new(a)
        models.storage.new(p)
        models.storage.new(r)

        self.assertIn(b, models.storage.all().values())
        self.assertIn(u, models.storage.all().values())
        self.assertIn(s, models.storage.all().values())
        self.assertIn(c, models.storage.all().values())
        self.assertIn(a, models.storage.all().values())
        self.assertIn(p, models.storage.all().values())
        self.assertIn(r, models.storage.all().values())

        self.assertIn(f"BaseModel.{b.id}", models.storage.all().keys())
        self.assertIn(f"User.{u.id}", models.storage.all().keys())
        self.assertIn(f"State.{s.id}", models.storage.all().keys())
        self.assertIn(f"City.{c.id}", models.storage.all().keys())
        self.assertIn(f"Amenity.{a.id}", models.storage.all().keys())
        self.assertIn(f"Place.{p.id}", models.storage.all().keys())
        self.assertIn(f"Review.{r.id}", models.storage.all().keys())

    def test_new_more_than_one_arg(self):
        b1 = BaseModel()
        b2 = BaseModel()
        with self.assertRaises(TypeError):
            models.storage.new(b1, b2)

    def test_save_no_args(self):
        b = BaseModel()
        u = User()
        s = State()
        c = City()
        a = Amenity()
        p = Place()
        r = Review()
        try:
            with open("file.json", "r", encoding="UTF8") as f:
                self.assertNotIn(f"BaseModel.{b.id}", f.read())
                self.assertNotIn(f"User.{u.id}", f.read())
                self.assertNotIn(f"State.{s.id}", f.read())
                self.assertNotIn(f"City.{c.id}", f.read())
                self.assertNotIn(f"Amenity.{a.id}", f.read())
                self.assertNotIn(f"Place.{p.id}", f.read())
                self.assertNotIn(f"Review.{r.id}", f.read())
        except FileNotFoundError:
            pass

        models.storage.save()
        with open("file.json", "r", encoding="UTF8") as f:
            json = f.read()
            self.assertIn(f"BaseModel.{b.id}", json)
            self.assertIn(f"User.{u.id}", json)
            self.assertIn(f"State.{s.id}", json)
            self.assertIn(f"City.{c.id}", json)
            self.assertIn(f"Amenity.{a.id}", json)
            self.assertIn(f"Place.{p.id}", json)
            self.assertIn(f"Review.{r.id}", json)

    def test_save_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.save("Invalid way")

    def test_reload_no_args(self):
        objects = FileStorage._FileStorage__objects
        b = BaseModel()
        u = User()
        s = State()
        c = City()
        a = Amenity()
        p = Place()
        r = Review()

        models.storage.save()
        models.storage.reload()
        self.assertIn(f'BaseModel.{b.id}', objects.keys())
        self.assertIn(f"User.{u.id}", objects.keys())
        self.assertIn(f"State.{s.id}", objects.keys())
        self.assertIn(f"City.{c.id}", objects.keys())
        self.assertIn(f"Amenity.{a.id}", objects.keys())
        self.assertIn(f"Place.{p.id}", objects.keys())
        self.assertIn(f"Review.{r.id}", objects.keys())

    def test_reload_one_args(self):
        with self.assertRaises(TypeError):
            models.storage.reload("Invalid")


if __name__ == "__main__":
    unittest.main()
