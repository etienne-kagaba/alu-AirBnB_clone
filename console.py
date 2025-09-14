#!/usr/bin/env python3
"""
Command interpreter for the AirBnB clone project.
"""

import cmd


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


if __name__ == '__main__':
    HBNBCommand().cmdloop()