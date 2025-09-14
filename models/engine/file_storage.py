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
    
    _FileStorage__file_path = "file.json"
    _FileStorage__objects = {}
    
    def __init__(self):
        """
        Initialize FileStorage instance.
        """
        # Make __file_path accessible as a regular attribute for testing
        # Use setattr to avoid name mangling
        setattr(self, '__file_path', "file.json")
    
    def all(self):
        """
        Return the dictionary __objects.
        
        Returns:
            dict: Dictionary containing all stored objects
        """
        return FileStorage._FileStorage__objects
    
    def new(self, obj):
        """
        Set in __objects the obj with key <obj class name>.id.
        
        Args:
            obj: Object to store
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage._FileStorage__objects[key] = obj
    
    def save(self):
        """
        Serialize __objects to the JSON file (path: __file_path).
        """
        objects_dict = {}
        for key, obj in FileStorage._FileStorage__objects.items():
            objects_dict[key] = obj.to_dict()
        
        with open(FileStorage._FileStorage__file_path, 'w', encoding='utf-8') as f:
            json.dump(objects_dict, f)
    
    def reload(self):
        """
        Deserialize the JSON file to __objects (only if the JSON file 
        (__file_path) exists; otherwise, do nothing. If the file doesn't 
        exist, no exception should be raised).
        """
        if os.path.exists(FileStorage._FileStorage__file_path):
            try:
                with open(FileStorage._FileStorage__file_path, 'r', encoding='utf-8') as f:
                    objects_dict = json.load(f)
                
                for key, obj_dict in objects_dict.items():
                    class_name = obj_dict['__class__']
                    # Import the class dynamically
                    if class_name == 'BaseModel':
                        from models.base_model import BaseModel
                        FileStorage._FileStorage__objects[key] = BaseModel(**obj_dict)
                    elif class_name == 'User':
                        from models.user import User
                        FileStorage._FileStorage__objects[key] = User(**obj_dict)
            except (json.JSONDecodeError, KeyError, ImportError):
                # If there's an error loading the file, start with empty objects
                FileStorage._FileStorage__objects = {}
