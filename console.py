#!/usr/bin/python3

""" This module contains the entry point of the command interpreter"""

import cmd
import models
import re
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
    classes = {"BaseModel", "User", "State", "City",
               "Amenity", "Place", "Review"}

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
        objects_list = []
        if not line:
            for obj in objects.values():
                objects_list.append(str(obj))
            print(objects_list)
        elif line in HBNBCommand.classes:
            for obj in objects.values():
                if obj.__class__.__name__ == line:
                    objects_list.append(str(obj))
            print(objects_list)
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
                    value_type = type(eval(args[3]))
                    setattr(objects[key], args[2], value_type(args[3]))
                    objects[key].save()

    def do_count(self, line):
        """Counts the number of instances of a class"""
        if not line:
            print("** class name missing **")
        elif line not in HBNBCommand.classes:
            print("** class doesn't exist **")
        else:
            objects = models.storage.all()
            count = 0
            for obj in objects.values():
                if obj.__class__.__name__ == line:
                    count += 1
            print(count)

    def default(self, line: str):
        """Default command to handle commands followed by a dot"""
        args = line.split(".")
        class_name = args[0]
        if len(args) == 1:
            print("***Unknown syntax: {}".format(line))
            return
        try:
            args = args[1].split("(")
            command = args[0]
            if command  == 'all':
                self.do_all(class_name)
            elif command == 'count':
                self.do_count(class_name)
            elif command == 'show':
                args = args[1].split(')')
                id_arg = args[0]
                id_arg = id_arg.strip("'")
                id_arg = id_arg.strip('"')
                line = class_name + ' ' + id_arg
                self.do_show(line)
            elif command == 'destroy':
                args = args[1].split(')')
                id_arg = args[0]
                id_arg = id_arg.strip("'")
                id_arg = id_arg.strip('"')
                line = class_name + ' ' + id_arg
                self.do_destroy(line)
            elif command == 'update':
                rx = r'(\{[^{}]+\})'
                dict_match = re.search(rx, args[1])
                if dict_match is None:     
                    args = args[1].split(', ')
                    id_arg = args[0].strip("'")
                    id_arg = id_arg.strip('"')

                    name_arg = args[1].strip(',')
                    val_arg = args[2]
                    name_arg = name_arg.strip(' ')
                    name_arg = name_arg.strip("'")
                    name_arg = name_arg.strip('"')
                    val_arg = val_arg.strip(' ')
                    val_arg = val_arg.strip(')')
                    val_arg = val_arg.strip("'")
                    val_arg = val_arg.strip('"')
                    line = class_name + ' ' + id_arg + ' ' + name_arg + ' ' + val_arg
                    self.do_update(line)
                else:
                    args = args[1].split(', ')
                    id_arg = args[0].strip("'")
                    id_arg = id_arg.strip('"')
                    for name_arg, val_arg in eval(dict_match.group(1)).items():
                        line = class_name + ' ' + id_arg + ' ' + name_arg + ' ' + val_arg
                        self.do_update(line)
            else:
                print("***Unknown syntax: {}".format(line))
        except IndexError:
            print("***Unknown syntax: {}".format(line))

        
if __name__ == "__main__":
    HBNBCommand().cmdloop()
