#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
    TestHBNBCommand_prompting
    TestHBNBCommand_help
    TestHBNBCommand_exit
    TestHBNBCommand_create
    TestHBNBCommand_show
    TestHBNBCommand_all
    TestHBNBCommand_destroy
    TestHBNBCommand_update
"""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class test_promting_command(unittest.TestCase):
    """Unittests for testing prompting of the HBNB command interpreter."""

    def test_prompt_string(self):
        self.assertEqual("(hbnb) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", foutput.getvalue().strip())


class test_help_command(unittest.TestCase):
    """Unittests for testing help messages of the HBNB command interpreter."""

    def test_help_quit(self):
        """
        Test the help quit function in the HBNB command.
        """
        msg = "Quit command to exit the program"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(msg, foutput.getvalue().strip())

    def test_help_create(self):
        """
        Test the help create function.
        """
        msg = ("Creates a new instance of BaseModel and prints its id")
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(msg, foutput.getvalue().strip())

    def test_help_EOF(self):
        """
        Test the help function with EOF signal to exit the program.
        """
        msg = "EOF command to exit the program"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(msg, foutput.getvalue().strip())

    def test_help_show(self):
        """
        A test case for the help_show method.
        """
        msg = ("Prints the string representation of an instance")
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("help show"))
            self.assertEqual(msg, foutput.getvalue().strip())

    def test_help_destroy(self):
        """
        A test function to check the functionality of the help destroy command.
        """
        msg = ("Deletes an instance based on the class name and id")
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(msg, foutput.getvalue().strip())

    def test_help_all(self):
        """
        Test the help all function.
        """
        msg = ("Prints all string representation of all instances")
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(msg, foutput.getvalue().strip())

    def test_help_count(self):
        """
        Test the help output for the count command.
        """
        msg = ("Counts the number of instances of a class")
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("help count"))
            self.assertEqual(msg, foutput.getvalue().strip())

    def test_help_update(self):
        """
        A test function to check the help update functionality.
        """
        msg = ("Updates an instance based on the class name and id")
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(msg, foutput.getvalue().strip())


class test_exit_command(unittest.TestCase):
    """Unittests for testing exiting from the HBNB command interpreter."""

    def test_quit_exits(self):
        """
        Test if the quit command exits the program.
        """
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        """
        Test if the EOF exits the function.
        """
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class test_create_command(unittest.TestCase):
    """Unittests for testing create from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_create_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_create_invalid_syntax(self):
        correct = "***Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(correct, foutput.getvalue().strip())
        correct = "***Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_create_object(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertLess(0, len(foutput.getvalue().strip()))
            testKey = "BaseModel.{}".format(foutput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertLess(0, len(foutput.getvalue().strip()))
            testKey = "User.{}".format(foutput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertLess(0, len(foutput.getvalue().strip()))
            testKey = "State.{}".format(foutput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertLess(0, len(foutput.getvalue().strip()))
            testKey = "City.{}".format(foutput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertLess(0, len(foutput.getvalue().strip()))
            testKey = "Amenity.{}".format(foutput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertLess(0, len(foutput.getvalue().strip()))
            testKey = "Place.{}".format(foutput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            self.assertLess(0, len(foutput.getvalue().strip()))
            testKey = "Review.{}".format(foutput.getvalue().strip())
            self.assertIn(testKey, storage.all().keys())


class test_show_command(unittest.TestCase):
    """Unittests for testing show from the HBNB command interpreter"""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_show_missing_class(self):
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd(".show()"))
            self.assertEqual("***Unknown syntax:", foutput.getvalue().strip())

    def test_show_invalid_class(self):
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show MyModel"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("MyModel.show()"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_show_missing_id_space_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show User"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show State"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show City"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show Amenity"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show Place"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show Review"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_show_missing_id_dot_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show()"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("User.show()"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("State.show()"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("City.show()"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show()"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Place.show()"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Review.show()"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_show_no_instance_found_space_notation(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show BaseModel 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show User 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show State 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show City 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show Amenity 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show Place 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("show Review 1"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_show_no_instance_found_dot_notation(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.show(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("User.show(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("State.show(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("City.show(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.show(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Place.show(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Review.show(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "show BaseModel {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["User.{}".format(testID)]
            command = "show User {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["State.{}".format(testID)]
            command = "show State {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["Place.{}".format(testID)]
            command = "show Place {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["City.{}".format(testID)]
            command = "show City {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "show Amenity {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["Review.{}".format(testID)]
            command = "show Review {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())

    def test_show_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "BaseModel.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["User.{}".format(testID)]
            command = "User.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["State.{}".format(testID)]
            command = "State.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["Place.{}".format(testID)]
            command = "Place.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["City.{}".format(testID)]
            command = "City.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "Amenity.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["Review.{}".format(testID)]
            command = "Review.show({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertEqual(obj.__str__(), foutput.getvalue().strip())


class test_destroy_command(unittest.TestCase):
    """Unittests for testing destroy from the HBNB command interpreter."""

    @classmethod
    def setUp(cls):
        """Set up the test environment."""
        try:
            # Rename file.json to tmp
            os.rename("file.json", "tmp")
        except IOError:
            # Ignore if file.json does not exist
            pass
        # Reset the __objects dictionary
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """
        A method to clean up resources after running tests.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        storage.reload()

    def test_missing_class(self):
        """
        Test for the case when the class name is missing.
        """
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd(".destroy()"))
            self.assertEqual("***Unknown syntax:", foutput.getvalue().strip())

    def test_invalid_class(self):
        """
        Test the behavior of destroying an invalid class.
        """
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy MyModel"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("MyModel.destroy()"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_destroy_id_missing_space_notation(self):
        """
        Test if destroy command works when id is missing.
        """
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy User"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy State"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy City"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy Place"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy Review"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_destroy_id_missing_dot_notation(self):
        correct = "** instance id missing **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy()"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("User.destroy()"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("State.destroy()"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("City.destroy()"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy()"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy()"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy()"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_destroy_invalid_id_space_notation(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy BaseModel 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy User 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy State 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy City 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy Amenity 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy Place 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("destroy Review 1"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_destroy_invalid_id_dot_notation(self):
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.destroy(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("User.destroy(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("State.destroy(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("City.destroy(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.destroy(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Place.destroy(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Review.destroy(1)"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_destroy_objects_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "destroy BaseModel {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["User.{}".format(testID)]
            command = "show User {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["State.{}".format(testID)]
            command = "show State {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["Place.{}".format(testID)]
            command = "show Place {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["City.{}".format(testID)]
            command = "show City {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "show Amenity {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["Review.{}".format(testID)]
            command = "show Review {}".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())

    def test_destroy_objects_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["BaseModel.{}".format(testID)]
            command = "BaseModel.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["User.{}".format(testID)]
            command = "User.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["State.{}".format(testID)]
            command = "State.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["Place.{}".format(testID)]
            command = "Place.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["City.{}".format(testID)]
            command = "City.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["Amenity.{}".format(testID)]
            command = "Amenity.destroy({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
            testID = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            obj = storage.all()["Review.{}".format(testID)]
            command = "Review.destory({})".format(testID)
            self.assertFalse(HBNBCommand().onecmd(command))
            self.assertNotIn(obj, storage.all())


class test_all_command(unittest.TestCase):
    """Unittests for testing all of the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        """
        Set up the test fixture. It's called before every test case method.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """
        A class method to tear down resources used in the test.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_all_invalid_class(self):
        """
        Test case for invalid class input in the HBNBCommand all method.
        """
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("all MyModel"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("MyModel.all()"))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_space_notation(self):
        """
        Test the creation of all objects.
        """
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("all"))
            self.assertIn("BaseModel", foutput.getvalue().strip())
            self.assertIn("User", foutput.getvalue().strip())
            self.assertIn("State", foutput.getvalue().strip())
            self.assertIn("Place", foutput.getvalue().strip())
            self.assertIn("City", foutput.getvalue().strip())
            self.assertIn("Amenity", foutput.getvalue().strip())
            self.assertIn("Review", foutput.getvalue().strip())

    def test_dot_notation(self):
        """
        Test the dot notation functionality for creating.
        """
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd(".all()"))
            self.assertIn("BaseModel", foutput.getvalue().strip())
            self.assertIn("User", foutput.getvalue().strip())
            self.assertIn("State", foutput.getvalue().strip())
            self.assertIn("Place", foutput.getvalue().strip())
            self.assertIn("City", foutput.getvalue().strip())
            self.assertIn("Amenity", foutput.getvalue().strip())
            self.assertIn("Review", foutput.getvalue().strip())

    def test_space_notation(self):
        """
        Test all single object space notation.
        """
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("all BaseModel"))
            self.assertIn("BaseModel", foutput.getvalue().strip())
            self.assertNotIn("User", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("all User"))
            self.assertIn("User", foutput.getvalue().strip())
            self.assertNotIn("BaseModel", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("all State"))
            self.assertIn("State", foutput.getvalue().strip())
            self.assertNotIn("BaseModel", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("all City"))
            self.assertIn("City", foutput.getvalue().strip())
            self.assertNotIn("BaseModel", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("all Amenity"))
            self.assertIn("Amenity", foutput.getvalue().strip())
            self.assertNotIn("BaseModel", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("all Place"))
            self.assertIn("Place", foutput.getvalue().strip())
            self.assertNotIn("BaseModel", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("all Review"))
            self.assertIn("Review", foutput.getvalue().strip())
            self.assertNotIn("BaseModel", foutput.getvalue().strip())

    def test_dot_notation(self):
        """
        Test all single object dot notation
        """
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            self.assertFalse(HBNBCommand().onecmd("create User"))
            self.assertFalse(HBNBCommand().onecmd("create State"))
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            self.assertFalse(HBNBCommand().onecmd("create City"))
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.all()"))
            self.assertIn("BaseModel", foutput.getvalue().strip())
            self.assertNotIn("User", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("User.all()"))
            self.assertIn("User", foutput.getvalue().strip())
            self.assertNotIn("BaseModel", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("State.all()"))
            self.assertIn("State", foutput.getvalue().strip())
            self.assertNotIn("BaseModel", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("City.all()"))
            self.assertIn("City", foutput.getvalue().strip())
            self.assertNotIn("BaseModel", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.all()"))
            self.assertIn("Amenity", foutput.getvalue().strip())
            self.assertNotIn("BaseModel", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Place.all()"))
            self.assertIn("Place", foutput.getvalue().strip())
            self.assertNotIn("BaseModel", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Review.all()"))
            self.assertIn("Review", foutput.getvalue().strip())
            self.assertNotIn("BaseModel", foutput.getvalue().strip())


class test_update_command(unittest.TestCase):
    """Unittests for testing update from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        """
        Set up the test fixture.It is called before each test function is run.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        """
        A method to clean up the test environment by removing temporary files.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_update_missingClass(self):
        """
        Test the behavior when the class name is missing in the update command.
        """
        correct = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("update"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd(".update()"))
            self.assertEqual("***Unknown syntax: .update()",
                             foutput.getvalue().strip())

    def test_update_invalidClass(self):
        """
        A test case for updating an invalid class.
        """
        correct = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("update MyModel"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("MyModel.update()"))
            self.assertEqual("***Unknown syntax: MyModel.update()",
                             foutput.getvalue().strip())

    def test_update_dotNotation(self):
        """
        Test for updating missing id in dot notation.
        """
        correct = "***Unknown syntax: "
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update()"))
            self.assertEqual(correct + "BaseModel.update()",
                             foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("User.update()"))
            self.assertEqual(correct + "User.update()",
                             foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("State.update()"))
            self.assertEqual(correct + "State.update()",
                             foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("City.update()"))
            self.assertEqual(correct + "City.update()",
                             foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update()"))
            self.assertEqual(correct + "Amenity.update()",
                             foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Place.update()"))
            self.assertEqual(correct + "Place.update()",
                             foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Review.update()"))
            self.assertEqual(correct + "Review.update()",
                             foutput.getvalue().strip())

    def test_update_invalid_id_space_notation(self):
        """
        Function to test updating with invalid id space notation.
        """
        correct = "** no instance found **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("update BaseModel 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("update User 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("update State 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("update City 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("update Amenity 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("update Place 1"))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("update Review 1"))
            self.assertEqual(correct, foutput.getvalue().strip())

        def test_update_spaceNotation(self):
            """
            Test for updating id space notation.
            """
            correct = "** instance id missing **"
            with patch("sys.stdout", new=StringIO()) as foutput:
                self.assertFalse(HBNBCommand().onecmd("update BaseModel"))
                self.assertEqual(correct, foutput.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as foutput:
                self.assertFalse(HBNBCommand().onecmd("update User"))
                self.assertEqual(correct, foutput.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as foutput:
                self.assertFalse(HBNBCommand().onecmd("update State"))
                self.assertEqual(correct, foutput.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as foutput:
                self.assertFalse(HBNBCommand().onecmd("update City"))
                self.assertEqual(correct, foutput.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as foutput:
                self.assertFalse(HBNBCommand().onecmd("update Amenity"))
                self.assertEqual(correct, foutput.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as foutput:
                self.assertFalse(HBNBCommand().onecmd("update Place"))
                self.assertEqual(correct, foutput.getvalue().strip())
            with patch("sys.stdout", new=StringIO()) as foutput:
                self.assertFalse(HBNBCommand().onecmd("update Review"))
                self.assertEqual(correct, foutput.getvalue().strip())

    def test_update_invalid_id_dot_notation(self):
        """
        Test for updating with invalid id using dot notation .
        """
        correct = "***Unknown syntax: "
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.update(1)"))
            self.assertEqual(correct + "BaseModel.update(1)",
                             foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("User.update(1)"))
            self.assertEqual(correct + "User.update(1)",
                             foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("State.update(1)"))
            self.assertEqual(correct + "State.update(1)",
                             foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("City.update(1)"))
            self.assertEqual(correct + "City.update(1)",
                             foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.update(1)"))
            self.assertEqual(correct + "Amenity.update(1)",
                             foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Place.update(1)"))
            self.assertEqual(correct + "Place.update(1)",
                             foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Review.update(1)"))
            self.assertEqual(correct + "Review.update(1)",
                             foutput.getvalue().strip())

    def test_update_missing_attr_value_space_notation(self):
        correct = "** value missing **"
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create BaseModel")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "update BaseModel {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create User")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "update User {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create State")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "update State {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create City")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "update City {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Amenity")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "update Amenity {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "update Place {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Review")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "update Review {} attr_name".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct, foutput.getvalue().strip())

    def test_update_missing_attr_value_dot_notation(self):
        correct = "***Unknown syntax: "
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create BaseModel")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "BaseModel.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct + testCmd, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create User")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "User.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct + testCmd, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create State")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "State.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct + testCmd, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create City")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "City.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct + testCmd, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Amenity")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "Amenity.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct + testCmd, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "Place.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct + testCmd, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Review")
            testId = foutput.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as foutput:
            testCmd = "Review.update({}, attr_name)".format(testId)
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct + testCmd, foutput.getvalue().strip())

    def test_update_missing_attr_name_dot_notation(self):
        correct = "***Unknown syntax: "
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
            testId = foutput.getvalue().strip()
            testCmd = "BaseModel.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct + testCmd, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
            testId = foutput.getvalue().strip()
            testCmd = "User.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct + testCmd, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
            testId = foutput.getvalue().strip()
            testCmd = "State.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct + testCmd, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
            testId = foutput.getvalue().strip()
            testCmd = "City.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct + testCmd, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
            testId = foutput.getvalue().strip()
            testCmd = "Amenity.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct + testCmd, foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
            testId = foutput.getvalue().strip()
            testCmd = "Place.update({})".format(testId)
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd(testCmd))
            self.assertEqual(correct + testCmd, foutput.getvalue().strip())

    def test_update_valid_string_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create BaseModel")
            testId = foutput.getvalue().strip()
        testCmd = "update BaseModel {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create User")
            testId = foutput.getvalue().strip()
        testCmd = "update User {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create State")
            testId = foutput.getvalue().strip()
        testCmd = "update State {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create City")
            testId = foutput.getvalue().strip()
        testCmd = "update City {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            testId = foutput.getvalue().strip()
        testCmd = "update Place {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Amenity")
            testId = foutput.getvalue().strip()
        testCmd = "update Amenity {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Review")
            testId = foutput.getvalue().strip()
        testCmd = "update Review {} attr_name 'attr_value'".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Review.{}".format(testId)].__dict__
        self.assertTrue("attr_value", test_dict["attr_name"])

    def test_update_valid_string_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create BaseModel")
            tId = foutput.getvalue().strip()
        testCmd = "BaseModel.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["BaseModel.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create User")
            tId = foutput.getvalue().strip()
        testCmd = "User.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["User.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create State")
            tId = foutput.getvalue().strip()
        testCmd = "State.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["State.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create City")
            tId = foutput.getvalue().strip()
        testCmd = "City.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["City.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            tId = foutput.getvalue().strip()
        testCmd = "Place.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Amenity")
            tId = foutput.getvalue().strip()
        testCmd = "Amenity.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Amenity.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Review")
            tId = foutput.getvalue().strip()
        testCmd = "Review.update({}, attr_name, 'attr_value')".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Review.{}".format(tId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_int_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            testId = foutput.getvalue().strip()
        testCmd = "update Place {} max_guest 98".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_int_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            tId = foutput.getvalue().strip()
        testCmd = "Place.update({}, max_guest, 98)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_float_attr_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            testId = foutput.getvalue().strip()
        testCmd = "update Place {} latitude 7.2".format(testId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_float_attr_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            tId = foutput.getvalue().strip()
        testCmd = "Place.update({}, latitude, 7.2)".format(tId)
        self.assertFalse(HBNBCommand().onecmd(testCmd))
        test_dict = storage.all()["Place.{}".format(tId)].__dict__
        self.assertEqual(7.2, test_dict["latitude"])

    def test_update_valid_dictionary_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create BaseModel")
            testId = foutput.getvalue().strip()
        testCmd = "BaseModel.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["BaseModel.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create User")
            testId = foutput.getvalue().strip()
        testCmd = "User.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create State")
            testId = foutput.getvalue().strip()
        testCmd = "State.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create City")
            testId = foutput.getvalue().strip()
        testCmd = "City.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            testId = foutput.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Amenity")
            testId = foutput.getvalue().strip()
        testCmd = "Amenity.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Review")
            testId = foutput.getvalue().strip()
        testCmd = "Review.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Review.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_dot_notation(self):

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create User")
            testId = foutput.getvalue().strip()
        testCmd = "User.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["User.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create State")
            testId = foutput.getvalue().strip()
        testCmd = "State.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["State.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create City")
            testId = foutput.getvalue().strip()
        testCmd = "City.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["City.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            testId = foutput.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Amenity")
            testId = foutput.getvalue().strip()
        testCmd = "Amenity.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Amenity.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Review")
            testId = foutput.getvalue().strip()
        testCmd = "Review.update({}, ".format(testId)
        testCmd += "{'attr_name': 'attr_value'})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Review.{}".format(testId)].__dict__
        self.assertEqual("attr_value", test_dict["attr_name"])

    def test_update_valid_dictionary_with_int_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            testId = foutput.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_int_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            testId = foutput.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'max_guest': 98})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(98, test_dict["max_guest"])

    def test_update_valid_dictionary_with_float_space_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            testId = foutput.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])

    def test_update_valid_dictionary_with_float_dot_notation(self):
        with patch("sys.stdout", new=StringIO()) as foutput:
            HBNBCommand().onecmd("create Place")
            testId = foutput.getvalue().strip()
        testCmd = "Place.update({}, ".format(testId)
        testCmd += "{'latitude': 9.8})"
        HBNBCommand().onecmd(testCmd)
        test_dict = storage.all()["Place.{}".format(testId)].__dict__
        self.assertEqual(9.8, test_dict["latitude"])


class test_count_command(unittest.TestCase):
    """Unittests for testing count method of HBNB comand interpreter."""

    @classmethod
    def setUp(self):
        """
        A method to set up the environment for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    @classmethod
    def tearDown(self):
        """
        A class method to clean up resources after running the tests.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_count_invalid_class(self):
        """
        Test the count method for invalid class.
        """
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("MyModel.count()"))
            self.assertEqual("** class doesn't exist **",
                             foutput.getvalue().strip())

    def test_countObject(self):
        """
        Test the count function for various model types and check the foutput
        """
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.count()"))
            self.assertEqual("1", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create User"))
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("User.count()"))
            self.assertEqual("1", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create State"))
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("State.count()"))
            self.assertEqual("1", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Place"))
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Place.count()"))
            self.assertEqual("1", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create City"))
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("City.count()"))
            self.assertEqual("1", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Amenity.count()"))
            self.assertEqual("1", foutput.getvalue().strip())
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("create Review"))
        with patch("sys.stdout", new=StringIO()) as foutput:
            self.assertFalse(HBNBCommand().onecmd("Review.count()"))
            self.assertEqual("1", foutput.getvalue().strip())


if __name__ == "__main__":
    unittest.main()
