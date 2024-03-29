#!/usr/bin/python3
"""
This file will contain Main console
"""
import cmd
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    Class that facilitates command line interpreter

    Attributes:
        - prompt (str): Command line message
        - support_models (list(str)) that contains supported models
    """

    prompt = "(hbnb) "
    support_models = [
        "BaseModel",
        "User",
        "Amenity",
        "City",
        "Place",
        "Review",
        "State",
    ]

    
    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing on an empty line"""
        pass

    def do_create(self, args):
        """
        Method that commits create command

        Args:
            - args (str): Input that represent the command input as in string.
        """
        # Check if arguments is empty
        if not args:
            print("** class name missing **")
            return False

        # Get arguments
        arguments = args.split(" ")
        # Best usecase for this is match case where as
        # if the model exists it operates
        if arguments[0] in self.support_models:
            # Initiate a new instance of base model
            new = eval(arguments[0])()
            print(new.id)
            # Don't forget to save
            new.save()
        else:
            # Default case in case the model entered is does not exist
            print("** class doesn't exist **")

    def do_show(self, args):
        """
        Method that commits show command

        Args:
            - args (str): Input that represent the command input as in string.
        """
        # Check if arguments is empty
        if not args:
            print("** class name missing **")
            return False
        
        # Get arguments
        arguments = args.split(" ")

        # Check if the model is supported or not
        if arguments[0] not in self.support_models:
            print("** class doesn't exist **")
            return False

        # Check if instance id exists or not
        if len(arguments) < 2:
            print("** instance id missing **")
            return False

        # Grab all instances
        instance = storage.find(arguments[0], arguments[1])
        # Check if instance exists
        if not instance:
            print("** no instance found **")
            return False

        print(instance)

    def do_destroy(self, args):
        """
        Method that commits destroy command

        Args:
            - args (str): Input that represent the command input as in string.
        """
        # Check if arguments is empty
        if not args:
            print("** class name missing **")
            return False

        # Get arguments
        arguments = args.split(" ")

        # Check if the model is supported or not
        if arguments[0] not in self.support_models:
            print("** class doesn't exist **")
            return False

        # Check if instance id exists or not
        if len(arguments) < 2:
            print("** instance id missing **")
            return False

        # Grab all instances
        instance = storage.find(arguments[0], arguments[1])
        # Check if instance exists
        if not instance:
            print("** no instance found **")
            return False

        # Destroy the model
        storage.delete(arguments[0], arguments[1])

    def do_all(self, args, printed = True):
        """
        Method that commits all command

        Args:
            - args (str): Input that represent the command input as in string.
        """
        # Get the models
        models = storage.all()

        # if no argument just print them
        if not args:
            # Store models in a list
            reformed = list(models.values())
            print([repr(element) for element in reformed])
        else:
            # Check if the model mention exists within
            if args not in self.support_models:
                print("** class doesn't exist **")
                return False
            # Print out the results
            models = [
                repr(element)
                for element in models.values()
                if element.__class__.__name__ == args
            ]
            if printed:
                print(models)
            return models

    def do_update(self, args):
        """
        Method that commits update command

        Args:
            - args (str): Input that represent the command input as in string.
        """
        # Check if arguments is empty
        if not args:
            print("** class name missing **")
            return False

        # Get arguments
        arguments = args.split(" ")

        # Check if the model is supported or not
        if arguments[0] not in self.support_models:
            print("** class doesn't exist **")
            return False

        # Check if instance id exists or not
        if len(arguments) < 2:
            print("** instance id missing **")
            return False

        # Grab all instances
        instance: object = storage.find(arguments[0], arguments[1])
        # Check if instance exists
        if not instance:
            print("** no instance found **")
            return False

        # Check if instance id exists or not
        if len(arguments) < 3:
            print("** attribute name missing **")
            return False

        # Check if instance id exists or not
        if len(arguments) < 4:
            print("** value missing **")
            return False

        parameter: str = arguments[2]
        value: str = arguments[3].replace('"', "").replace("'", "")

        # update/set attribute
        setattr(instance, parameter, value)
        instance.save()

    def updated_helper(self, model, args):
        """
        Helper method to execute update method in many ways
        """
        if "{" in args:
            # Treat it as there is a dictionary
            arguments = args.split("{")
            updates = "{" + arguments[1]
            object_id: str = arguments[0].replace(",", "")\
                .strip().replace("\"", "")
            updates = json.loads(updates)
            for key in updates:
                command: str = " ".join(
                    [model, object_id, key, str(updates[key])]
                )
                self.do_update(command)
        else:
            command = " ".join(
                [
                    element.strip().replace("\"", "")
                    for element in args.split(",")
                ]
            )
            command = model + " " + command
            self.do_update(command)

    def default(self, args):
        """
        Method to handle defaults
        """
        # Check if there is a Dot in the args
        if "." in args:
            # Split model and command type by dots
            args = args.split(".")
            # Model should be at start for instance User
            model: str = args[0]
            # Get the command should be for instance all()
            command = ".".join(args[1:]).split("(")
            # Grabing function name
            command_func: str = command[0]
            if command_func != "update":
                arguments: str = command[1].replace(")", "").replace("\"", "")
            else:
                arguments: str = command[1].replace(")", "")
            # Check function
            if command_func == 'all':
                self.do_all(model)
            elif command_func == 'count':
                print(len(self.do_all(model, False)))
            elif command_func == 'show':
                argument: str = " ".join([model, arguments])
                self.do_show(argument)
            elif command_func == "destroy":
                argument: str = " ".join([model, arguments])
                self.do_destroy(argument)
            elif command_func == "update":
                self.updated_helper(model, arguments)
            
            return False
        print("*** Unknown syntax: {}".format(args))
        return False


if __name__ == "__main__":
    HBNBCommand().cmdloop()
