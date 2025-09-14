#!/usr/bin/env python3
"""
Command interpreter for the AirBnB clone project.
"""

import cmd
import sys
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    Command interpreter class for the AirBnB clone project.
    """
    
    prompt = "(hbnb) "
    
    def emptyline(self):
        """
        Do nothing when an empty line is entered.
        """
        return False
    
    def do_quit(self, arg):
        """
        Quit command to exit the program
        """
        return True
    
    def do_EOF(self, arg):
        """
        EOF command to exit the program
        """
        print()
        return True
    
    def do_create(self, arg):
        """
        Creates a new instance of BaseModel, saves it and prints the id.
        Usage: create <class name>
        """
        if not arg:
            print("** class name missing **")
            return
        
        class_name = arg.strip()
        if class_name != "BaseModel":
            print("** class doesn't exist **")
            return
        
        new_instance = BaseModel()
        new_instance.save()
        print(new_instance.id)
    
    def do_show(self, arg):
        """
        Prints the string representation of an instance.
        Usage: show <class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        
        class_name = args[0]
        if class_name != "BaseModel":
            print("** class doesn't exist **")
            return
        
        if len(args) < 2:
            print("** instance id missing **")
            return
        
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        objects = storage.all()
        
        if key not in objects:
            print("** no instance found **")
            return
        
        print(objects[key])
    
    def do_destroy(self, arg):
        """
        Deletes an instance based on class name and id.
        Usage: destroy <class name> <id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        
        class_name = args[0]
        if class_name != "BaseModel":
            print("** class doesn't exist **")
            return
        
        if len(args) < 2:
            print("** instance id missing **")
            return
        
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        objects = storage.all()
        
        if key not in objects:
            print("** no instance found **")
            return
        
        del objects[key]
        storage.save()
    
    def do_all(self, arg):
        """
        Prints all string representation of all instances.
        Usage: all [<class name>]
        """
        objects = storage.all()
        
        if arg:
            class_name = arg.strip()
            if class_name != "BaseModel":
                print("** class doesn't exist **")
                return
            
            # Filter objects by class name
            filtered_objects = []
            for key, obj in objects.items():
                if obj.__class__.__name__ == class_name:
                    filtered_objects.append(str(obj))
            print(filtered_objects)
        else:
            # Print all objects
            all_objects = [str(obj) for obj in objects.values()]
            print(all_objects)
    
    def do_update(self, arg):
        """
        Updates an instance based on class name and id.
        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        
        class_name = args[0]
        if class_name != "BaseModel":
            print("** class doesn't exist **")
            return
        
        if len(args) < 2:
            print("** instance id missing **")
            return
        
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        objects = storage.all()
        
        if key not in objects:
            print("** no instance found **")
            return
        
        if len(args) < 3:
            print("** attribute name missing **")
            return
        
        if len(args) < 4:
            print("** value missing **")
            return
        
        attr_name = args[2]
        attr_value = args[3]
        
        # Remove quotes if present
        if attr_value.startswith('"') and attr_value.endswith('"'):
            attr_value = attr_value[1:-1]
        
        # Get the object and update the attribute
        obj = objects[key]
        
        # Try to convert to int or float if possible
        try:
            if '.' in attr_value:
                attr_value = float(attr_value)
            else:
                attr_value = int(attr_value)
        except ValueError:
            # Keep as string if conversion fails
            pass
        
        setattr(obj, attr_name, attr_value)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()