import unittest
from unittest.mock import patch
from io import StringIO
from models import storage
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State


class TestHBNBCommand(unittest.TestCase):
    def setUp(self):
        self.console = HBNBCommand()

    def tearDown(self):
        """
        Method to clean up and reset the state after running tests.
        No parameters and no return type.
        """
        storage.delete_all()

    def test_quit(self):
        """
        Test the quit functionality of the console method and verify the output.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertTrue(self.console.onecmd("quit"))
            self.assertEqual(fake_out.getvalue(), "")

    def test_EOF(self):
        """
        Test the EOF function with  asserting the output and the return value.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertTrue(self.console.onecmd("EOF"))
            self.assertEqual(fake_out.getvalue(), "\n")

    def test_emptyline(self):
        """
        Test the behavior of the function when an empty line is passed as input.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("")
            self.assertEqual(fake_out.getvalue(), "")

    def test_create_missing_class(self):
        """
        Test the behavior of creating a missing class.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("create")
            self.assertEqual(fake_out.getvalue(), "** class name missing **\n")

    def test_create_invalid_class(self):
        """
        A test for creating an invalid class.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("create InvalidClass")
            self.assertEqual(fake_out.getvalue(), "** class doesn't exist **\n")

    def test_create_valid_class(self):
        """
        Test for creating a valid class.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("create BaseModel")
            output = fake_out.getvalue().strip()
            self.assertIsNotNone(output)
            self.assertIsInstance(storage.get(output), BaseModel)

    def test_show_missing_class(self):
        """
        Test for showing missing class.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("show")
            self.assertEqual(fake_out.getvalue(), "** class name missing **\n")

    def test_show_invalid_class(self):
        """
        Test case for showing invalid class.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("show InvalidClass")
            self.assertEqual(fake_out.getvalue(), "** class doesn't exist **\n")

    def test_show_missing_id(self):
        """
        Test function to check if the show method handles missing instance id .
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("show BaseModel")
            self.assertEqual(fake_out.getvalue(), "** instance id missing **\n")

    def test_show_invalid_id(self):
        """
        A test function to show behavior when an invalid ID is provided.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("show BaseModel 12345")
            self.assertEqual(fake_out.getvalue(), "** no instance found **\n")

    def test_show_valid_instance(self):
        """
        Test the show method with a valid instance.
        """
        obj = BaseModel()
        obj.save()
        obj_id = obj.id
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd(f"show BaseModel {obj_id}")
            output = fake_out.getvalue().strip()
            self.assertEqual(output, str(obj))

    def test_destroy_missing_class(self):
        """
        A test case for class name is missing in the destroy command.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("destroy")
            self.assertEqual(fake_out.getvalue(), "** class name missing **\n")

    def test_destroy_invalid_class(self):
        """
        Test for destroying an invalid class.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("destroy InvalidClass")
            self.assertEqual(fake_out.getvalue(), "** class doesn't exist **\n")

    def test_destroy_missing_id(self):
        """
        Test case for checking the behavior when the ID is missing .
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("destroy BaseModel")
            self.assertEqual(fake_out.getvalue(), "** instance id missing **\n")

    def test_destroy_invalid_id(self):
        """
        Test the behavior of destroying an invalid ID.
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd("destroy BaseModel 12345")
            self.assertEqual(fake_out.getvalue(), "** no instance found **\n")

    def test_destroy_valid_instance(self):
        """
        Test for destroying a valid instance.
        """
        obj = BaseModel()
        obj.save()
        obj_id = obj.id
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.console.onecmd(f"destroy BaseModel {obj_id}")
            self.assertEqual(fake_out.getvalue(), "")
            self.assertIsNone(storage.get("BaseModel", obj_id))

    # Add more test cases for other commands...

if __name__ == '__main__':
    unittest.main()