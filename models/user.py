#!/usr/bin/python3
"""
User class for AirBnB clone project.

This module contains the User class that inherits from BaseModel
and defines user-specific attributes.
"""

from models.base_model import BaseModel


class User(BaseModel):
    """
    User class that inherits from BaseModel.
    
    Public class attributes:
        email: string - empty string
        password: string - empty string
        first_name: string - empty string
        last_name: string - empty string
    """
    
    email = ""
    password = ""
    first_name = ""
    last_name = ""
