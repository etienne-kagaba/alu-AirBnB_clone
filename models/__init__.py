#!/usr/bin/python3
"""
Models package for AirBnB clone project.

This package contains all the model classes for the AirBnB clone project,
including the BaseModel class and all derived classes.
"""

from models.engine.file_storage import FileStorage

# Create a unique FileStorage instance for the application
storage = FileStorage()

# Call reload() method on this variable
storage.reload()
