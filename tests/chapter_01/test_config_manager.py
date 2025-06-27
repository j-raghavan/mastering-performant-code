"""
Unit tests for ConfigurationManager implementation.

This module provides comprehensive test coverage for the ConfigurationManager class,
including configuration operations, validation, and memory analysis.
"""

import unittest
import tempfile
import os
import json
from typing import Dict, Any

from mastering_performant_code.chapter_01.config_manager import ConfigurationManager, ConfigItem

class TestConfigurationManager(unittest.TestCase):
    """Test cases for ConfigurationManager implementation."""
    
    def setUp(self):
        self.config_mgr = ConfigurationManager()
    
    def test_initialization(self):
        """Test configuration manager initialization."""
        self.assertEqual(len(self.config_mgr._configs), 0)
        self.assertEqual(len(self.config_mgr._tags), 0)
        self.assertEqual(len(self.config_mgr._history), 0)
    
    def test_set_get_config(self):
        """Test set and get configuration operations."""
        self.config_mgr.set_config("database.host", "localhost", "Database host address")
        
        value = self.config_mgr.get_config("database.host")
        self.assertEqual(value, "localhost")
        
        # Test non-existent key
        value = self.config_mgr.get_config("missing.key")
        self.assertIsNone(value)
    
    def test_set_config_with_tags(self):
        """Test set configuration with tags."""
        self.config_mgr.set_config(
            "database.port", 
            5432, 
            "Database port number",
            {"database", "network"}
        )
        
        value = self.config_mgr.get_config("database.port")
        self.assertEqual(value, 5432)
        
        # Check tags
        database_configs = self.config_mgr.get_by_tag("database")
        self.assertIn("database.port", database_configs)
        
        network_configs = self.config_mgr.get_by_tag("network")
        self.assertIn("database.port", network_configs)
    
    def test_delete_config(self):
        """Test delete configuration operation."""
        self.config_mgr.set_config("test.key", "test_value")
        
        # Delete existing key
        result = self.config_mgr.delete_config("test.key")
        self.assertTrue(result)
        
        # Verify deletion
        value = self.config_mgr.get_config("test.key")
        self.assertIsNone(value)
        
        # Delete non-existent key
        result = self.config_mgr.delete_config("missing.key")
        self.assertFalse(result)
    
    def test_delete_config_with_tags(self):
        """Test delete configuration with tags."""
        self.config_mgr.set_config(
            "app.debug", 
            True, 
            "Debug mode flag",
            {"app", "development"}
        )
        
        # Delete the config
        self.config_mgr.delete_config("app.debug")
        
        # Check that tags are cleaned up
        app_configs = self.config_mgr.get_by_tag("app")
        self.assertEqual(len(app_configs), 0)
        
        development_configs = self.config_mgr.get_by_tag("development")
        self.assertEqual(len(development_configs), 0)
    
    def test_get_by_tag(self):
        """Test get configurations by tag."""
        self.config_mgr.set_config("db.host", "localhost", tags={"database"})
        self.config_mgr.set_config("db.port", 5432, tags={"database"})
        self.config_mgr.set_config("app.name", "MyApp", tags={"app"})
        
        database_configs = self.config_mgr.get_by_tag("database")
        self.assertEqual(set(database_configs), {"db.host", "db.port"})
        
        app_configs = self.config_mgr.get_by_tag("app")
        self.assertEqual(set(app_configs), {"app.name"})
        
        # Non-existent tag
        missing_configs = self.config_mgr.get_by_tag("missing")
        self.assertEqual(missing_configs, [])
    
    def test_search_configs(self):
        """Test search configurations."""
        self.config_mgr.set_config("database.host", "localhost", "Database host address")
        self.config_mgr.set_config("database.port", 5432, "Database port number")
        self.config_mgr.set_config("app.name", "MyApp", "Application name")
        
        # Search by key
        results = self.config_mgr.search_configs("database")
        self.assertEqual(set(results), {"database.host", "database.port"})
        
        # Search by description
        results = self.config_mgr.search_configs("address")
        self.assertEqual(set(results), {"database.host"})
        
        # Case insensitive search
        results = self.config_mgr.search_configs("DATABASE")
        self.assertEqual(set(results), {"database.host", "database.port"})
        
        # Non-existent search
        results = self.config_mgr.search_configs("missing")
        self.assertEqual(results, [])
    
    def test_get_history(self):
        """Test get configuration history."""
        self.config_mgr.set_config("key1", "value1")
        self.config_mgr.set_config("key2", "value2")
        self.config_mgr.delete_config("key1")
        
        history = self.config_mgr.get_history()
        self.assertEqual(len(history), 3)
        
        # Check history entries
        self.assertEqual(history[0]["action"], "set")
        self.assertEqual(history[0]["key"], "key1")
        self.assertEqual(history[0]["value"], "value1")
        
        self.assertEqual(history[1]["action"], "set")
        self.assertEqual(history[1]["key"], "key2")
        self.assertEqual(history[1]["value"], "value2")
        
        self.assertEqual(history[2]["action"], "delete")
        self.assertEqual(history[2]["key"], "key1")
    
    def test_get_history_limit(self):
        """Test get configuration history with limit."""
        # Add many configurations
        for i in range(20):
            self.config_mgr.set_config(f"key{i}", f"value{i}")
        
        # Get limited history
        history = self.config_mgr.get_history(limit=5)
        self.assertEqual(len(history), 5)
        
        # Check that we get the most recent entries
        self.assertEqual(history[0]["key"], "key15")
        self.assertEqual(history[4]["key"], "key19")
    
    def test_export_import_json(self):
        """Test export and import JSON functionality."""
        # Add configurations
        self.config_mgr.set_config(
            "database.host", 
            "localhost", 
            "Database host address",
            {"database", "network"}
        )
        self.config_mgr.set_config(
            "app.debug", 
            True, 
            "Debug mode flag",
            {"app", "development"}
        )
        
        # Export to JSON
        json_data = self.config_mgr.export_json()
        self.assertIsInstance(json_data, str)
        
        # Parse JSON to verify structure
        config_data = json.loads(json_data)
        self.assertIn("database.host", config_data)
        self.assertIn("app.debug", config_data)
        
        self.assertEqual(config_data["database.host"]["value"], "localhost")
        self.assertEqual(config_data["database.host"]["description"], "Database host address")
        self.assertEqual(set(config_data["database.host"]["tags"]), {"database", "network"})
        
        # Import JSON
        new_config_mgr = ConfigurationManager()
        new_config_mgr.import_json(json_data)
        
        # Verify imported data
        self.assertEqual(new_config_mgr.get_config("database.host"), "localhost")
        self.assertEqual(new_config_mgr.get_config("app.debug"), True)
        
        database_configs = new_config_mgr.get_by_tag("database")
        self.assertIn("database.host", database_configs)
    
    def test_get_memory_stats(self):
        """Test get memory statistics."""
        # Add some configurations
        self.config_mgr.set_config("key1", "value1", tags={"tag1"})
        self.config_mgr.set_config("key2", "value2", tags={"tag2"})
        
        stats = self.config_mgr.get_memory_stats()
        
        self.assertIsInstance(stats, dict)
        self.assertIn("configs", stats)
        self.assertIn("tags", stats)
        self.assertIn("history", stats)
        self.assertIn("total_memory", stats)
        
        # Check configs stats
        configs_stats = stats["configs"]
        self.assertEqual(configs_stats["size"], 2)
        self.assertGreater(configs_stats["memory"], 0)
        self.assertGreaterEqual(configs_stats["load_factor"], 0)
        self.assertLessEqual(configs_stats["load_factor"], 1)
        
        # Check tags stats
        tags_stats = stats["tags"]
        self.assertEqual(tags_stats["size"], 2)
        self.assertGreater(tags_stats["memory"], 0)
        
        # Check history stats
        history_stats = stats["history"]
        self.assertEqual(history_stats["size"], 2)
        self.assertGreater(history_stats["memory"], 0)
        
        # Check total memory
        self.assertGreater(stats["total_memory"], 0)


class TestConfigItem(unittest.TestCase):
    """Test cases for ConfigItem dataclass."""
    
    def test_config_item_creation(self):
        """Test ConfigItem creation."""
        item = ConfigItem(
            key="test.key",
            value="test_value",
            description="Test description",
            tags={"tag1", "tag2"}
        )
        
        self.assertEqual(item.key, "test.key")
        self.assertEqual(item.value, "test_value")
        self.assertEqual(item.description, "Test description")
        self.assertEqual(item.tags, {"tag1", "tag2"})
        self.assertIsInstance(item.created_at, float)
        self.assertIsInstance(item.updated_at, float)
    
    def test_config_item_defaults(self):
        """Test ConfigItem with default values."""
        item = ConfigItem(key="test.key", value="test_value")
        
        self.assertEqual(item.key, "test.key")
        self.assertEqual(item.value, "test_value")
        self.assertEqual(item.description, "")
        self.assertEqual(item.tags, set())
        self.assertIsInstance(item.created_at, float)
        self.assertIsInstance(item.updated_at, float)


class TestConfigurationManagerEdgeCases(unittest.TestCase):
    """Edge case tests for ConfigurationManager."""
    
    def setUp(self):
        from mastering_performant_code.chapter_01.config_manager import ConfigurationManager
        self.config_mgr = ConfigurationManager()
    
    def test_empty_config_manager(self):
        """Test operations on empty configuration manager."""
        self.assertEqual(len(self.config_mgr._configs), 0)
        self.assertEqual(len(self.config_mgr._tags), 0)
        self.assertEqual(len(self.config_mgr._history), 0)
        
        # Test operations on empty manager
        self.assertIsNone(self.config_mgr.get_config("missing"))
        self.assertFalse(self.config_mgr.delete_config("missing"))
        self.assertEqual(self.config_mgr.get_by_tag("missing"), [])
        self.assertEqual(self.config_mgr.search_configs("missing"), [])
        self.assertEqual(self.config_mgr.get_history(), [])
        
        # Export empty manager
        json_data = self.config_mgr.export_json()
        self.assertEqual(json_data, "{}")
    
    def test_large_number_of_configs(self):
        """Test with a large number of configurations."""
        # Add many configurations
        for i in range(1000):
            self.config_mgr.set_config(
                f"key{i}", 
                f"value{i}", 
                f"Description for key{i}",
                {f"tag{i % 10}"}  # 10 different tags
            )
        
        self.assertEqual(len(self.config_mgr._configs), 1000)
        self.assertEqual(len(self.config_mgr._tags), 10)
        self.assertEqual(len(self.config_mgr._history), 1000)
        
        # Test retrieval
        self.assertEqual(self.config_mgr.get_config("key500"), "value500")
        
        # Test tag retrieval
        tag0_configs = self.config_mgr.get_by_tag("tag0")
        self.assertEqual(len(tag0_configs), 100)  # Every 10th config
        
        # Test search
        results = self.config_mgr.search_configs("key500")
        self.assertEqual(results, ["key500"])
    
    def test_none_values(self):
        """Test handling of None values."""
        self.config_mgr.set_config("none.key", None, "None value")
        
        value = self.config_mgr.get_config("none.key")
        self.assertIsNone(value)
    
    def test_complex_values(self):
        """Test handling of complex values."""
        complex_value = {
            "nested": {
                "list": [1, 2, 3],
                "string": "hello"
            },
            "number": 42
        }
        
        self.config_mgr.set_config("complex.key", complex_value, "Complex value")
        
        value = self.config_mgr.get_config("complex.key")
        self.assertEqual(value, complex_value)
    
    def test_unicode_values(self):
        """Test handling of Unicode values."""
        unicode_key = "测试.key"
        unicode_value = "测试值"
        unicode_description = "测试描述"
        
        self.config_mgr.set_config(
            unicode_key, 
            unicode_value, 
            unicode_description,
            {"测试", "tag"}
        )
        
        value = self.config_mgr.get_config(unicode_key)
        self.assertEqual(value, unicode_value)
        
        # Test search with Unicode
        results = self.config_mgr.search_configs("测试")
        self.assertIn(unicode_key, results)
        
        # Test tag with Unicode
        tag_configs = self.config_mgr.get_by_tag("测试")
        self.assertIn(unicode_key, tag_configs)


if __name__ == '__main__':
    unittest.main(verbosity=2) 