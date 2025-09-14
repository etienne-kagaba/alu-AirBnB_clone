#!/usr/bin/python3
"""
BaseModel class for AirBnB clone project.

This module contains the BaseModel class that defines all common
attributes and methods for other classes in the AirBnB clone project.
"""

import uuid
from datetime import datetime
from models import storage


class BaseModel:
    """
    BaseModel class that defines all common attributes/methods for other classes.
    """
    
    def __init__(self, *args, **kwargs):
        """
        Initialize BaseModel instance.
        
        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    # Convert string back to datetime object
                    setattr(self, key, datetime.fromisoformat(value))
                elif key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            # Add new instance to storage
            storage.new(self)
    
    def __str__(self):
        """
        String representation of the BaseModel instance.
        
        Returns:
            str: Formatted string representation
        """
        return "[{}] ({}) {}".format(
            self.__class__.__name__,
            self.id,
            self.__dict__
        )
    
    def save(self):
        """
        Update the public instance attribute updated_at with the current datetime
        and save the object to storage.
        """
        self.updated_at = datetime.now()
        storage.save()
    
    def to_dict(self):
        """
        Return a dictionary containing all keys/values of __dict__ of the instance.
        
        Returns:
            dict: Dictionary representation of the instance
        """
        dict_copy = self.__dict__.copy()
        dict_copy['__class__'] = self.__class__.__name__
        dict_copy['created_at'] = self.created_at.isoformat()
        dict_copy['updated_at'] = self.updated_at.isoformat()
        return dict_copy
