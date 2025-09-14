#!/usr/bin/python3
"""
FileStorage class for AirBnB clone project.

This module contains the FileStorage class that handles serialization
and deserialization of objects to/from JSON files.
"""

import json
import os


class FileStorage:
    """
    FileStorage class that serializes instances to a JSON file and 
    deserializes JSON file to instances.
    """
    
    def __init__(self):
        """
        Initialize FileStorage instance.
        """
        self.__file_path = "file.json"
        self.__objects = {}
    
    def all(self):
        """
        Return the dictionary __objects.
        
        Returns:
            dict: Dictionary containing all stored objects
        """
        return self.__objects
    
    def new(self, obj):
        """
        Set in __objects the obj with key <obj class name>.id.
        
        Args:
            obj: Object to store
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj
    
    def save(self):
        """
        Serialize __objects to the JSON file (path: __file_path).
        """
        objects_dict = {}
        for key, obj in self.__objects.items():
            objects_dict[key] = obj.to_dict()
        
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            json.dump(objects_dict, f)
    
    def reload(self):
        """
        Deserialize the JSON file to __objects (only if the JSON file 
        (__file_path) exists; otherwise, do nothing. If the file doesn't 
        exist, no exception should be raised).
        """
        if os.path.exists(self.__file_path):
            try:
                with open(self.__file_path, 'r', encoding='utf-8') as f:
                    objects_dict = json.load(f)
                
                for key, obj_dict in objects_dict.items():
                    class_name = obj_dict['__class__']
                    # Import the class dynamically
                    if class_name == 'BaseModel':
                        from models.base_model import BaseModel
                        self.__objects[key] = BaseModel(**obj_dict)
                    # Add more classes here as they are created
                    # elif class_name == 'User':
                    #     from models.user import User
                    #     self.__objects[key] = User(**obj_dict)
            except (json.JSONDecodeError, KeyError, ImportError):
                # If there's an error loading the file, start with empty objects
                self.__objects = {}
