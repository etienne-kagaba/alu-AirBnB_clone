#!/usr/bin/python3
"""
Unit tests for BaseModel class.

This module contains comprehensive unit tests for the BaseModel class
to ensure all functionality works as expected.
"""

import unittest
import json
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):
    """
    Test cases for BaseModel class.
    
    This class contains all unit tests for the BaseModel class,
    testing initialization, serialization, deserialization, and methods.
    """
    
    def setUp(self):
        """
        Set up test fixtures before each test method.
        """
        self.base_model = BaseModel()
    
    def test_init_no_args(self):
        """
        Test BaseModel initialization with no arguments.
        """
        self.assertIsInstance(self.base_model, BaseModel)
        self.assertIsInstance(self.base_model.id, str)
        self.assertIsInstance(self.base_model.created_at, datetime)
        self.assertIsInstance(self.base_model.updated_at, datetime)
        # created_at and updated_at should be very close (within 1 second)
        time_diff = abs((self.base_model.updated_at - self.base_model.created_at).total_seconds())
        self.assertLess(time_diff, 1.0)
    
    def test_init_with_kwargs(self):
        """
        Test BaseModel initialization with keyword arguments.
        """
        test_dict = {
            'id': 'test-id-123',
            'created_at': '2023-01-01T12:00:00.000000',
            'updated_at': '2023-01-01T13:00:00.000000',
            'name': 'Test Model',
            'number': 42
        }
        
        model = BaseModel(**test_dict)
        
        self.assertEqual(model.id, 'test-id-123')
        self.assertEqual(model.name, 'Test Model')
        self.assertEqual(model.number, 42)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)
    
    def test_init_with_class_key(self):
        """
        Test BaseModel initialization ignores __class__ key.
        """
        test_dict = {
            'id': 'test-id-456',
            '__class__': 'SomeOtherClass',
            'name': 'Test Model'
        }
        
        model = BaseModel(**test_dict)
        
        self.assertEqual(model.id, 'test-id-456')
        self.assertEqual(model.name, 'Test Model')
        self.assertNotEqual(model.__class__.__name__, 'SomeOtherClass')
        self.assertEqual(model.__class__.__name__, 'BaseModel')
    
    def test_unique_ids(self):
        """
        Test that each BaseModel instance has a unique ID.
        """
        model1 = BaseModel()
        model2 = BaseModel()
        model3 = BaseModel()
        
        self.assertNotEqual(model1.id, model2.id)
        self.assertNotEqual(model1.id, model3.id)
        self.assertNotEqual(model2.id, model3.id)
    
    def test_str_representation(self):
        """
        Test the string representation of BaseModel.
        """
        expected_format = "[BaseModel] ({}) {}".format(
            self.base_model.id, self.base_model.__dict__
        )
        self.assertEqual(str(self.base_model), expected_format)
    
    def test_str_with_attributes(self):
        """
        Test string representation with additional attributes.
        """
        self.base_model.name = "My First Model"
        self.base_model.my_number = 89
        
        expected_format = "[BaseModel] ({}) {}".format(
            self.base_model.id, self.base_model.__dict__
        )
        self.assertEqual(str(self.base_model), expected_format)
    
    def test_save_updates_updated_at(self):
        """
        Test that save method updates the updated_at attribute.
        """
        original_updated_at = self.base_model.updated_at
        
        # Wait a small amount to ensure time difference
        import time
        time.sleep(0.001)
        
        self.base_model.save()
        
        self.assertGreater(self.base_model.updated_at, original_updated_at)
        self.assertEqual(self.base_model.created_at, self.base_model.created_at)
    
    def test_to_dict_structure(self):
        """
        Test the structure of the dictionary returned by to_dict.
        """
        self.base_model.name = "Test Model"
        self.base_model.number = 42
        
        model_dict = self.base_model.to_dict()
        
        # Check required keys
        self.assertIn('id', model_dict)
        self.assertIn('created_at', model_dict)
        self.assertIn('updated_at', model_dict)
        self.assertIn('__class__', model_dict)
        self.assertIn('name', model_dict)
        self.assertIn('number', model_dict)
        
        # Check __class__ value
        self.assertEqual(model_dict['__class__'], 'BaseModel')
        
        # Check that datetime fields are strings
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)
    
    def test_to_dict_datetime_format(self):
        """
        Test that datetime fields in to_dict are in ISO format.
        """
        model_dict = self.base_model.to_dict()
        
        # Parse the datetime strings back to datetime objects
        created_at_parsed = datetime.fromisoformat(model_dict['created_at'])
        updated_at_parsed = datetime.fromisoformat(model_dict['updated_at'])
        
        # Check that parsed datetimes match original
        self.assertEqual(created_at_parsed, self.base_model.created_at)
        self.assertEqual(updated_at_parsed, self.base_model.updated_at)
    
    def test_to_dict_roundtrip(self):
        """
        Test that to_dict and reconstruction from dict work correctly.
        """
        # Add some attributes
        self.base_model.name = "Roundtrip Test"
        self.base_model.value = 100
        
        # Convert to dict and back
        model_dict = self.base_model.to_dict()
        new_model = BaseModel(**model_dict)
        
        # Check that all attributes match
        self.assertEqual(new_model.id, self.base_model.id)
        self.assertEqual(new_model.name, self.base_model.name)
        self.assertEqual(new_model.value, self.base_model.value)
        self.assertEqual(new_model.created_at, self.base_model.created_at)
        self.assertEqual(new_model.updated_at, self.base_model.updated_at)
    
    def test_to_dict_excludes_class_attribute(self):
        """
        Test that to_dict doesn't include __class__ in the instance dict.
        """
        model_dict = self.base_model.to_dict()
        
        # The __class__ key should be added by to_dict, not from __dict__
        self.assertIn('__class__', model_dict)
        self.assertEqual(model_dict['__class__'], 'BaseModel')
    
    def test_instance_attributes_only(self):
        """
        Test that to_dict only includes instance attributes.
        """
        # Add instance attributes
        self.base_model.name = "Instance Test"
        self.base_model.number = 99
        
        model_dict = self.base_model.to_dict()
        
        # Should include instance attributes
        self.assertIn('name', model_dict)
        self.assertIn('number', model_dict)
        self.assertEqual(model_dict['name'], "Instance Test")
        self.assertEqual(model_dict['number'], 99)
    
    def test_json_serialization(self):
        """
        Test that the dictionary from to_dict is JSON serializable.
        """
        self.base_model.name = "JSON Test"
        self.base_model.number = 77
        
        model_dict = self.base_model.to_dict()
        
        # Should be able to serialize to JSON
        json_str = json.dumps(model_dict)
        self.assertIsInstance(json_str, str)
        
        # Should be able to deserialize from JSON
        parsed_dict = json.loads(json_str)
        self.assertEqual(parsed_dict, model_dict)
    
    def test_datetime_iso_format(self):
        """
        Test that datetime fields use the correct ISO format.
        """
        model_dict = self.base_model.to_dict()
        
        # Check format matches expected pattern: YYYY-MM-DDTHH:MM:SS.ffffff
        import re
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}$'
        
        self.assertRegex(model_dict['created_at'], iso_pattern)
        self.assertRegex(model_dict['updated_at'], iso_pattern)
    
    def test_multiple_instances_independence(self):
        """
        Test that multiple instances are independent.
        """
        model1 = BaseModel()
        model2 = BaseModel()
        
        # Add different attributes
        model1.name = "Model 1"
        model2.name = "Model 2"
        
        # Check independence
        self.assertNotEqual(model1.id, model2.id)
        self.assertNotEqual(model1.name, model2.name)
        self.assertNotEqual(model1.created_at, model2.created_at)
    
    def test_dict_reconstruction_with_class_key(self):
        """
        Test that __class__ key is properly ignored during reconstruction.
        """
        original_model = BaseModel()
        original_model.name = "Test Model"
        original_model.value = 42
        
        # Convert to dict and add __class__ key
        model_dict = original_model.to_dict()
        model_dict['__class__'] = 'SomeOtherClass'
        
        # Reconstruct from dict
        new_model = BaseModel(**model_dict)
        
        # Check that __class__ was ignored
        self.assertEqual(new_model.__class__.__name__, 'BaseModel')
        self.assertNotEqual(new_model.__class__.__name__, 'SomeOtherClass')
        self.assertEqual(new_model.name, "Test Model")
        self.assertEqual(new_model.value, 42)
    
    def test_dict_reconstruction_datetime_conversion(self):
        """
        Test that datetime strings are properly converted back to datetime objects.
        """
        original_model = BaseModel()
        original_model.name = "DateTime Test"
        
        # Convert to dict
        model_dict = original_model.to_dict()
        
        # Verify datetime fields are strings in dict
        self.assertIsInstance(model_dict['created_at'], str)
        self.assertIsInstance(model_dict['updated_at'], str)
        
        # Reconstruct from dict
        new_model = BaseModel(**model_dict)
        
        # Verify datetime fields are datetime objects in new model
        self.assertIsInstance(new_model.created_at, datetime)
        self.assertIsInstance(new_model.updated_at, datetime)
        
        # Verify they match the original
        self.assertEqual(new_model.created_at, original_model.created_at)
        self.assertEqual(new_model.updated_at, original_model.updated_at)
    
    def test_dict_reconstruction_preserves_all_attributes(self):
        """
        Test that all attributes are preserved during dictionary reconstruction.
        """
        original_model = BaseModel()
        original_model.name = "Attribute Test"
        original_model.number = 123
        original_model.boolean = True
        original_model.list_attr = [1, 2, 3]
        original_model.dict_attr = {'key': 'value'}
        
        # Convert to dict and back
        model_dict = original_model.to_dict()
        new_model = BaseModel(**model_dict)
        
        # Check all attributes are preserved
        self.assertEqual(new_model.name, "Attribute Test")
        self.assertEqual(new_model.number, 123)
        self.assertEqual(new_model.boolean, True)
        self.assertEqual(new_model.list_attr, [1, 2, 3])
        self.assertEqual(new_model.dict_attr, {'key': 'value'})
        self.assertEqual(new_model.id, original_model.id)
        self.assertEqual(new_model.created_at, original_model.created_at)
        self.assertEqual(new_model.updated_at, original_model.updated_at)
    
    def test_dict_reconstruction_creates_different_instance(self):
        """
        Test that reconstruction creates a different instance (not the same object).
        """
        original_model = BaseModel()
        original_model.name = "Instance Test"
        
        # Convert to dict and back
        model_dict = original_model.to_dict()
        new_model = BaseModel(**model_dict)
        
        # Should be different instances
        self.assertIsNot(original_model, new_model)
        self.assertFalse(original_model is new_model)
        
        # But should have same attributes
        self.assertEqual(original_model.id, new_model.id)
        self.assertEqual(original_model.name, new_model.name)
    
    def test_dict_reconstruction_with_empty_kwargs(self):
        """
        Test that reconstruction with empty kwargs creates new instance.
        """
        # Create with empty kwargs
        model = BaseModel(**{})
        
        # Should have new id and timestamps
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)
    
    def test_save_preserves_other_attributes(self):
        """
        Test that save method preserves other instance attributes.
        """
        self.base_model.name = "Preserve Test"
        self.base_model.value = 123
        
        original_name = self.base_model.name
        original_value = self.base_model.value
        original_id = self.base_model.id
        original_created_at = self.base_model.created_at
        
        self.base_model.save()
        
        # Check that other attributes are preserved
        self.assertEqual(self.base_model.name, original_name)
        self.assertEqual(self.base_model.value, original_value)
        self.assertEqual(self.base_model.id, original_id)
        self.assertEqual(self.base_model.created_at, original_created_at)


if __name__ == '__main__':
    unittest.main()
