"""
Unit tests for Database Index implementation.

This module provides comprehensive tests for the DatabaseIndex class,
ensuring all database operations work correctly with AVL tree indexing.
"""

import pytest
import os
import tempfile
import json

from chapter_07.database_index import DatabaseIndex

class TestDatabaseIndex:
    """Test cases for DatabaseIndex class."""
    
    def test_empty_database(self):
        """Test empty database properties."""
        db = DatabaseIndex()
        assert len(db._data) == 0
        assert db._next_id == 1
        assert db.get_all_records() == []
        assert db.get_index_stats()['total_records'] == 0
    
    def test_insert_single_record(self):
        """Test inserting a single record."""
        db = DatabaseIndex()
        record = {"name": "Alice", "age": 25, "city": "New York"}
        
        record_id = db.insert_record(record)
        
        assert record_id == 1
        assert len(db._data) == 1
        assert db._data[1] == record
        assert db._next_id == 2
        
        # Check index stats
        stats = db.get_index_stats()
        assert stats['total_records'] == 1
        assert stats['index_size'] > 0  # Should have index entries for each field
        assert stats['is_balanced'] is True
    
    def test_insert_multiple_records(self):
        """Test inserting multiple records."""
        db = DatabaseIndex()
        records = [
            {"name": "Alice", "age": 25, "city": "New York"},
            {"name": "Bob", "age": 30, "city": "Los Angeles"},
            {"name": "Charlie", "age": 35, "city": "Chicago"}
        ]
        
        record_ids = []
        for record in records:
            record_id = db.insert_record(record)
            record_ids.append(record_id)
        
        assert record_ids == [1, 2, 3]
        assert len(db._data) == 3
        assert db._next_id == 4
        
        # Check that all records are stored
        for i, record in enumerate(records):
            assert db._data[record_ids[i]] == record
    
    def test_search_by_field_exact_match(self):
        """Test searching by field with exact match."""
        db = DatabaseIndex()
        records = [
            {"name": "Alice", "age": 25, "city": "New York"},
            {"name": "Bob", "age": 30, "city": "Los Angeles"},
            {"name": "Charlie", "age": 35, "city": "New York"}
        ]
        
        for record in records:
            db.insert_record(record)
        
        # Search by city
        ny_people = db.search_by_field("city", "New York")
        assert len(ny_people) == 2
        assert any(person["name"] == "Alice" for person in ny_people)
        assert any(person["name"] == "Charlie" for person in ny_people)
        
        # Search by age
        age_30_people = db.search_by_field("age", 30)
        assert len(age_30_people) == 1
        assert age_30_people[0]["name"] == "Bob"
        
        # Search by name
        alice_records = db.search_by_field("name", "Alice")
        assert len(alice_records) == 1
        assert alice_records[0]["age"] == 25
    
    def test_search_by_field_no_match(self):
        """Test searching by field with no matches."""
        db = DatabaseIndex()
        records = [
            {"name": "Alice", "age": 25, "city": "New York"},
            {"name": "Bob", "age": 30, "city": "Los Angeles"}
        ]
        
        for record in records:
            db.insert_record(record)
        
        # Search for non-existing values
        results = db.search_by_field("city", "Boston")
        assert len(results) == 0
        
        results = db.search_by_field("age", 40)
        assert len(results) == 0
        
        results = db.search_by_field("name", "David")
        assert len(results) == 0
    
    def test_range_query(self):
        """Test range queries."""
        db = DatabaseIndex()
        records = [
            {"name": "Alice", "age": 25, "salary": 50000},
            {"name": "Bob", "age": 30, "salary": 60000},
            {"name": "Charlie", "age": 35, "salary": 70000},
            {"name": "Diana", "age": 28, "salary": 55000},
            {"name": "Eve", "age": 32, "salary": 65000}
        ]
        
        for record in records:
            db.insert_record(record)
        
        # Range query on age
        young_people = db.range_query("age", 25, 30)
        assert len(young_people) == 3  # Alice (25), Bob (30), Diana (28)
        
        # Range query on salary
        high_earners = db.range_query("salary", 60000, 70000)
        assert len(high_earners) == 3  # Bob (60000), Charlie (70000), Eve (65000)
        
        # Range query with no matches
        no_matches = db.range_query("age", 40, 50)
        assert len(no_matches) == 0
    
    def test_delete_record(self):
        """Test deleting records."""
        db = DatabaseIndex()
        records = [
            {"name": "Alice", "age": 25, "city": "New York"},
            {"name": "Bob", "age": 30, "city": "Los Angeles"},
            {"name": "Charlie", "age": 35, "city": "Chicago"}
        ]
        
        record_ids = []
        for record in records:
            record_id = db.insert_record(record)
            record_ids.append(record_id)
        
        initial_size = len(db._data)
        
        # Delete a record
        result = db.delete_record(record_ids[1])  # Delete Bob
        assert result is True
        assert len(db._data) == initial_size - 1
        assert record_ids[1] not in db._data
        
        # Verify the record is gone
        bob_records = db.search_by_field("name", "Bob")
        assert len(bob_records) == 0
        
        # Verify other records are still there
        alice_records = db.search_by_field("name", "Alice")
        assert len(alice_records) == 1
        
        charlie_records = db.search_by_field("name", "Charlie")
        assert len(charlie_records) == 1
    
    def test_delete_non_existing_record(self):
        """Test deleting a non-existing record."""
        db = DatabaseIndex()
        record = {"name": "Alice", "age": 25}
        db.insert_record(record)
        
        # Try to delete non-existing record
        result = db.delete_record(999)
        assert result is False
        assert len(db._data) == 1  # Size should not change
    
    def test_get_all_records(self):
        """Test getting all records."""
        db = DatabaseIndex()
        records = [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30},
            {"name": "Charlie", "age": 35}
        ]
        
        for record in records:
            db.insert_record(record)
        
        all_records = db.get_all_records()
        assert len(all_records) == 3
        
        # Check that all records are present
        for record in records:
            assert record in all_records
    
    def test_get_index_stats(self):
        """Test getting index statistics."""
        db = DatabaseIndex()
        records = [
            {"name": "Alice", "age": 25, "city": "New York"},
            {"name": "Bob", "age": 30, "city": "Los Angeles"}
        ]
        
        for record in records:
            db.insert_record(record)
        
        stats = db.get_index_stats()
        
        assert stats['total_records'] == 2
        assert stats['index_size'] > 0  # Should have index entries
        assert stats['index_height'] > 0
        assert stats['is_balanced'] is True
    
    def test_export_and_import_json(self):
        """Test exporting and importing database to/from JSON."""
        db = DatabaseIndex()
        records = [
            {"name": "Alice", "age": 25, "city": "New York"},
            {"name": "Bob", "age": 30, "city": "Los Angeles"}
        ]
        
        for record in records:
            db.insert_record(record)
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_filename = f.name
        
        try:
            db.export_to_json(temp_filename)
            
            # Create new database and import
            new_db = DatabaseIndex()
            new_db.import_from_json(temp_filename)
            
            # Verify data integrity
            assert len(new_db._data) == len(db._data)
            assert new_db._next_id == db._next_id
            
            # Verify all records are present
            for record_id, record in db._data.items():
                assert new_db._data[record_id] == record
            
            # Verify index is working
            alice_records = new_db.search_by_field("name", "Alice")
            assert len(alice_records) == 1
            assert alice_records[0]["age"] == 25
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_get_field_values(self):
        """Test getting unique field values."""
        db = DatabaseIndex()
        records = [
            {"name": "Alice", "age": 25, "city": "New York"},
            {"name": "Bob", "age": 30, "city": "Los Angeles"},
            {"name": "Charlie", "age": 25, "city": "New York"},
            {"name": "Diana", "age": 35, "city": "Chicago"}
        ]
        
        for record in records:
            db.insert_record(record)
        
        # Get unique cities
        cities = db.get_field_values("city")
        assert set(cities) == {"New York", "Los Angeles", "Chicago"}
        
        # Get unique ages
        ages = db.get_field_values("age")
        assert set(ages) == {25, 30, 35}
        
        # Get unique names
        names = db.get_field_values("name")
        assert set(names) == {"Alice", "Bob", "Charlie", "Diana"}
    
    def test_get_field_statistics(self):
        """Test getting field statistics."""
        db = DatabaseIndex()
        records = [
            {"name": "Alice", "age": 25, "salary": 50000},
            {"name": "Bob", "age": 30, "salary": 60000},
            {"name": "Charlie", "age": 35, "salary": 70000},
            {"name": "Diana", "age": 25, "salary": 55000}
        ]
        
        for record in records:
            db.insert_record(record)
        
        # Test age statistics
        age_stats = db.get_field_statistics("age")
        assert age_stats['field_name'] == "age"
        assert age_stats['count'] == 4
        assert age_stats['unique_values'] == 3
        assert age_stats['min'] == 25
        assert age_stats['max'] == 35
        assert age_stats['numeric_min'] == 25
        assert age_stats['numeric_max'] == 35
        assert age_stats['numeric_count'] == 4
        
        # Test salary statistics
        salary_stats = db.get_field_statistics("salary")
        assert salary_stats['field_name'] == "salary"
        assert salary_stats['count'] == 4
        assert salary_stats['unique_values'] == 4
        assert salary_stats['min'] == 50000
        assert salary_stats['max'] == 70000
        assert salary_stats['numeric_min'] == 50000
        assert salary_stats['numeric_max'] == 70000
        assert salary_stats['numeric_count'] == 4
        
        # Test name statistics (non-numeric)
        name_stats = db.get_field_statistics("name")
        assert name_stats['field_name'] == "name"
        assert name_stats['count'] == 4
        assert name_stats['unique_values'] == 4
        assert name_stats['min'] == "Alice"  # String comparison
        assert name_stats['max'] == "Diana"
        assert 'numeric_min' not in name_stats  # Should not have numeric stats
    
    def test_get_field_statistics_empty_field(self):
        """Test getting statistics for empty field."""
        db = DatabaseIndex()
        record = {"name": "Alice", "age": 25}
        db.insert_record(record)
        
        # Test statistics for non-existent field
        stats = db.get_field_statistics("nonexistent")
        assert stats['field_name'] == "nonexistent"
        assert stats['count'] == 0
        assert stats['unique_values'] == 0
        assert stats['min'] is None
        assert stats['max'] is None
    
    def test_handle_different_data_types(self):
        """Test handling different data types in records."""
        db = DatabaseIndex()
        records = [
            {"name": "Alice", "age": 25, "salary": 50000.5, "active": True},
            {"name": "Bob", "age": 30, "salary": 60000.0, "active": False}
        ]
        
        for record in records:
            db.insert_record(record)
        
        # Test searching by different data types
        active_people = db.search_by_field("active", True)
        assert len(active_people) == 1
        assert active_people[0]["name"] == "Alice"
        
        inactive_people = db.search_by_field("active", False)
        assert len(inactive_people) == 1
        assert inactive_people[0]["name"] == "Bob"
        
        # Test range query on float
        high_salary = db.range_query("salary", 55000.0, 65000.0)
        assert len(high_salary) == 1
        assert high_salary[0]["name"] == "Bob"
    
    def test_handle_non_indexable_fields(self):
        """Test handling fields that are not indexable."""
        db = DatabaseIndex()
        records = [
            {"name": "Alice", "age": 25, "data": {"key": "value"}},
            {"name": "Bob", "age": 30, "data": [1, 2, 3]}
        ]
        
        for record in records:
            db.insert_record(record)
        
        # Non-indexable fields should not be indexed
        stats = db.get_index_stats()
        # Should only have index entries for name and age (not data)
        assert stats['index_size'] == 4  # 2 records * 2 indexable fields
        
        # Should still be able to search by indexable fields
        alice_records = db.search_by_field("name", "Alice")
        assert len(alice_records) == 1
        assert alice_records[0]["data"] == {"key": "value"}
    
    def test_concurrent_operations(self):
        """Test multiple operations on the same database."""
        db = DatabaseIndex()
        
        # Insert records
        record1_id = db.insert_record({"name": "Alice", "age": 25})
        record2_id = db.insert_record({"name": "Bob", "age": 30})
        
        # Search
        alice_records = db.search_by_field("name", "Alice")
        assert len(alice_records) == 1
        
        # Update (delete and reinsert)
        db.delete_record(record1_id)
        new_record1_id = db.insert_record({"name": "Alice", "age": 26})
        
        # Search again
        alice_records = db.search_by_field("name", "Alice")
        assert len(alice_records) == 1
        assert alice_records[0]["age"] == 26
        
        # Range query
        young_people = db.range_query("age", 25, 30)
        assert len(young_people) == 2  # Alice (26) and Bob (30)
        
        # Get statistics
        stats = db.get_index_stats()
        assert stats['total_records'] == 2
        assert stats['is_balanced'] is True 