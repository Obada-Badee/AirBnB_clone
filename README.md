<h1 align="center">AirBnB clone</h1>

<p align="center">
  <img src="https://github.com/Obada-Badee/AirBnB_clone/blob/master/assets/hbnb-logo.png"
       width="500"
  >
</p>

## Table of Contents

- [Description](#Description)
- [Storage engine](#Storage engine)
- [Command Interpreter](#Command Interpreter)
- [How to Start the Console](#How to Start the Console)
- [Examples](#Examples)

## Description :house:
The Airbnb Console is a A command interpreter to manipulate data without a visual interface, like in a Shell (perfect for development and debugging). The ALX Airbnb Console provides a convenient way to create your data model, manage(create, update, destroy, etc) and manipulate data related to Airbnb users, store and persist data to a file (JSON file).

## Storage engine

The first piece is to manipulate a powerful storage system. This storage engine will give us an abstraction between “My object” and “How they are stored and persisted”. This means: from the console code (the command interpreter itself) and from the front-end and RestAPI, we won’t have to pay attention (take care) of how our objects are stored.
This abstraction will also allow us to change the type of storage easily without updating all of our codebase.
The console will be a tool to validate this storage engine.

## Command Interpreter (Console)

The ALX Airbnb Console is built on a command interpreter that allows users to interact with the system through a series of commands. Here's how to start and use the console:

## How to Start the Console :grey_question:

To start the ALX Airbnb Console, follow these steps:

1. Clone the project repository from GitHub: [ALX Airbnb Console](https://github.com/Obada-Badee/AirBnB_clone.git).
2. Run the console application using the command:
   `$ python console.py` or
   `$ ./console.py` but make sure that console.py have execute permissions.
3. To run the ALX Airbnb Console in the non-interactive mode, you can use the following approach:
   `$ echo "help" | ./console.py`

This command will execute the console script, and the output will be displayed as follows:
```
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
```

Alternatively, you can also provide a file containing the command as input. For example, if you have a file named test_help with the content help, you can use the following command:
`cat test_help | ./console.py`

The output will be the same as above:
```
(hbnb)

Documented commands (type help <topic>):
========================================
EOF  help  quit
(hbnb)
```

Feel free to explore and interact with the ALX Airbnb Console.

## Examples

Once the console is running, you can enter commands and interact with the ALX Airbnb system. The general syntax for a command is:
command_name [arguments]

Here are some example commands that you can use:

1. `create`: Creates a new instance of a class, saves it (to the JSON file) and prints the `id`.

	Syntax: `create <class name>`

	Ex: `$ create BaseModel`
   
2. `show`: Prints the string representation of an instance based on the class name and `id`.

	Syntax: `show <class name> <id>`

	Ex: `$ show BaseModel 1234-1234-1234`

3. `update`: Updates an instance based on the class name and id by adding or updating attribute (save the change into the JSON file).

	Syntax: `update <class name> <id> <attribute name> "<attribute value>"`

	Ex: `$ update BaseModel 1234-1234-1234 email "aibnb@mail.com"`.

4. `destroy`: Deletes an instance based on the class name and `id` (save the change into the JSON file).

	syntax: `destroy <class name> <id>`

	Ex: `$ destroy BaseModel 1234-1234-1234`.
   
5. `all`: Prints all string representation of all instances based or not on the class name.

	syntax: `all [class name]`

	Ex: `$ all BaseModel` or `$ all`.
