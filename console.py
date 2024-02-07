#!/usr/bin/python3

""" This module contains the entry point of the command interpreter"""

import cmd
import models
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class HBNBCommand(cmd.Cmd):
    """The HBNB command interpreter"""

    prompt = "(hbnb) "
    classes = {BaseModel, User, State, City, Amenity,
               Place, Review}

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """An empty line shouldn't execute anything"""
        pass

    def do_create(self, line):
        """Creates a new instance of BaseModel and prints its id"""
        if not line:
            print("** class name missing **")
        elif line not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            object = eval(line)()
            object.save()
            print(object.id)
    
    def do_show(self, line):
        """Prints the string representation of an instance"""
        if not line:
            print("** class name missing **")
        else:
            args = line.split()
            if args[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                objects = models.storage.all()
                if key not in objects.keys():
                    print("** no instance found **")
                else:
                    print(objects[key])

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""
        if not line:
            print("** class name missing **")
        else:
            args = line.split()
            if args[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                objects = models.storage.all()
                if key not in objects.keys():
                    print("** no instance found **")
                else:
                    del objects[key]
                    models.storage.save()
    
    def do_all(self, line):
        """Prints all string representation of all instances"""
        objects = models.storage.all()
        if not line:
            for obj in objects.values():
                print(obj)
        elif line in HBNBCommand.classes:
            for obj in objects.values():
                if obj.__class__.__name__ == line:
                    print(obj)
        else:
            print("** class doesn't exist **")

    def do_update(self, line):
        """Updates an instance based on the class name and id"""
        if not line:
            print("** class name missing **")
        else:
            args = line.split()
            if args[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(args[0], args[1])
                objects = models.storage.all()
                if key not in objects.keys():
                    print("** no instance found **")
                elif len(args) < 3:
                    print("** attribute name missing **")
                elif len(args) < 4:
                    print("** value missing **")
                else:
                    objects[key].__dict__[args[2]] = args[3]
                    objects[key].save()

if __name__ == "__main__":
    HBNBCommand().cmdloop()
