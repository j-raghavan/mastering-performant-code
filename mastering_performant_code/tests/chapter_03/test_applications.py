"""
Unit tests for real-world applications of dynamic arrays.

This module provides comprehensive tests for TextBuffer, SimpleDatabase,
and CircularBuffer to ensure correct functionality.
"""

import pytest
from typing import List
from chapter_03.applications import (
    TextBuffer,
    DatabaseRecord,
    SimpleDatabase,
    CircularBuffer
)


class TestTextBuffer:
    """Test cases for the TextBuffer class."""
    
    def test_init(self):
        """Test initialization."""
        buffer = TextBuffer()
        assert buffer.line_count() == 0
        assert buffer.get_cursor_position() == (0, 0)
    
    def test_insert_line(self):
        """Test inserting a line."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello, World!")
        
        assert buffer.line_count() == 1
        assert buffer.get_line(0) == "Hello, World!"
    
    def test_insert_line_invalid_index(self):
        """Test inserting line at invalid index."""
        buffer = TextBuffer()
        
        with pytest.raises(IndexError, match="Line number 1 out of range"):
            buffer.insert_line(1, "Hello")
    
    def test_delete_line(self):
        """Test deleting a line."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Line 1")
        buffer.insert_line(1, "Line 2")
        buffer.insert_line(2, "Line 3")
        
        deleted = buffer.delete_line(1)
        assert deleted == "Line 2"
        assert buffer.line_count() == 2
        assert buffer.get_line(0) == "Line 1"
        assert buffer.get_line(1) == "Line 3"
    
    def test_delete_line_invalid_index(self):
        """Test deleting line at invalid index."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello")
        
        with pytest.raises(IndexError, match="Line number 1 out of range"):
            buffer.delete_line(1)
    
    def test_get_line(self):
        """Test getting a line."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello, World!")
        
        assert buffer.get_line(0) == "Hello, World!"
    
    def test_get_line_invalid_index(self):
        """Test getting line at invalid index."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello")
        
        with pytest.raises(IndexError, match="Line number 1 out of range"):
            buffer.get_line(1)
    
    def test_set_line(self):
        """Test setting a line."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Original")
        
        buffer.set_line(0, "Modified")
        assert buffer.get_line(0) == "Modified"
    
    def test_set_line_invalid_index(self):
        """Test setting line at invalid index."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello")
        
        with pytest.raises(IndexError, match="Line number 1 out of range"):
            buffer.set_line(1, "Modified")
    
    def test_get_all_lines(self):
        """Test getting all lines."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Line 1")
        buffer.insert_line(1, "Line 2")
        buffer.insert_line(2, "Line 3")
        
        lines = buffer.get_all_lines()
        assert lines == ["Line 1", "Line 2", "Line 3"]
    
    def test_line_count(self):
        """Test line count."""
        buffer = TextBuffer()
        assert buffer.line_count() == 0
        
        buffer.insert_line(0, "Line 1")
        assert buffer.line_count() == 1
        
        buffer.insert_line(1, "Line 2")
        assert buffer.line_count() == 2
    
    def test_append_line(self):
        """Test appending a line."""
        buffer = TextBuffer()
        buffer.append_line("Line 1")
        buffer.append_line("Line 2")
        
        assert buffer.line_count() == 2
        assert buffer.get_line(0) == "Line 1"
        assert buffer.get_line(1) == "Line 2"
    
    def test_insert_text(self):
        """Test inserting text in a line."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello World")
        
        buffer.insert_text(0, 5, ", Beautiful")
        assert buffer.get_line(0) == "Hello, Beautiful World"
    
    def test_insert_text_invalid_line(self):
        """Test inserting text in invalid line."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello")
        
        with pytest.raises(IndexError, match="Line number 1 out of range"):
            buffer.insert_text(1, 0, "World")
    
    def test_insert_text_invalid_column(self):
        """Test inserting text at invalid column."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello")
        
        with pytest.raises(IndexError, match="Column 6 out of range for line 0"):
            buffer.insert_text(0, 6, "World")
    
    def test_delete_text(self):
        """Test deleting text from a line."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello, Beautiful World")
        
        deleted = buffer.delete_text(0, 5, 16)
        assert deleted == ", Beautiful"
        assert buffer.get_line(0) == "Hello World"
    
    def test_delete_text_invalid_line(self):
        """Test deleting text from invalid line."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello")
        
        with pytest.raises(IndexError, match="Line number 1 out of range"):
            buffer.delete_text(1, 0, 1)
    
    def test_delete_text_invalid_range(self):
        """Test deleting text with invalid range."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello")
        
        with pytest.raises(IndexError, match="Invalid column range: 3-2"):
            buffer.delete_text(0, 3, 2)
    
    def test_set_cursor(self):
        """Test setting cursor position."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello, World!")
        
        buffer.set_cursor(0, 5)
        assert buffer.get_cursor_position() == (0, 5)
    
    def test_set_cursor_invalid_line(self):
        """Test setting cursor at invalid line."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello")
        
        with pytest.raises(IndexError, match="Line number 1 out of range"):
            buffer.set_cursor(1, 0)
    
    def test_set_cursor_invalid_column(self):
        """Test setting cursor at invalid column."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello")
        
        with pytest.raises(IndexError, match="Column 6 out of range for line 0"):
            buffer.set_cursor(0, 6)
    
    def test_cursor_position_updates_on_insert(self):
        """Test that cursor position updates when inserting lines."""
        buffer = TextBuffer()
        buffer.set_cursor(0, 0)
        
        buffer.insert_line(0, "New line")
        assert buffer.get_cursor_position() == (1, 0)
    
    def test_cursor_position_updates_on_delete(self):
        """Test that cursor position updates when deleting lines."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Line 1")
        buffer.insert_line(1, "Line 2")
        buffer.set_cursor(1, 0)
        
        buffer.delete_line(0)
        assert buffer.get_cursor_position() == (0, 0)
    
    def test_repr(self):
        """Test string representation."""
        buffer = TextBuffer()
        buffer.insert_line(0, "Hello")
        buffer.set_cursor(0, 3)
        
        assert repr(buffer) == "TextBuffer(1 lines, cursor at (0, 3))"


class TestDatabaseRecord:
    """Test cases for the DatabaseRecord class."""
    
    def test_init(self):
        """Test initialization."""
        record = DatabaseRecord(1, "Test", 42.5)
        assert record.id == 1
        assert record.name == "Test"
        assert record.value == 42.5
    
    def test_repr(self):
        """Test string representation."""
        record = DatabaseRecord(1, "Test", 42.5)
        assert repr(record) == "Record(id=1, name='Test', value=42.5)"
    
    def test_eq_same_record(self):
        """Test equality with same record."""
        record1 = DatabaseRecord(1, "Test", 42.5)
        record2 = DatabaseRecord(1, "Test", 42.5)
        assert record1 == record2
    
    def test_eq_different_record(self):
        """Test equality with different record."""
        record1 = DatabaseRecord(1, "Test", 42.5)
        record2 = DatabaseRecord(2, "Test", 42.5)
        assert record1 != record2
    
    def test_eq_different_type(self):
        """Test equality with different type."""
        record = DatabaseRecord(1, "Test", 42.5)
        assert record != "not a record"
    
    def test_hash(self):
        """Test hash function."""
        record1 = DatabaseRecord(1, "Test", 42.5)
        record2 = DatabaseRecord(1, "Test", 42.5)
        assert hash(record1) == hash(record2)


class TestSimpleDatabase:
    """Test cases for the SimpleDatabase class."""
    
    def test_init(self):
        """Test initialization."""
        db = SimpleDatabase()
        assert db.record_count() == 0
    
    def test_insert(self):
        """Test inserting a record."""
        db = SimpleDatabase()
        record_id = db.insert("Test", 42.5)
        
        assert record_id == 1
        assert db.record_count() == 1
    
    def test_get_by_id_existing(self):
        """Test getting record by existing ID."""
        db = SimpleDatabase()
        record_id = db.insert("Test", 42.5)
        
        record = db.get_by_id(record_id)
        assert record is not None
        assert record.id == record_id
        assert record.name == "Test"
        assert record.value == 42.5
    
    def test_get_by_id_nonexistent(self):
        """Test getting record by non-existent ID."""
        db = SimpleDatabase()
        record = db.get_by_id(1)
        assert record is None
    
    def test_get_by_name(self):
        """Test getting records by name."""
        db = SimpleDatabase()
        db.insert("Test", 42.5)
        db.insert("Test", 43.0)
        db.insert("Other", 44.0)
        
        records = db.get_by_name("Test")
        assert len(records) == 2
        assert all(record.name == "Test" for record in records)
    
    def test_get_by_name_nonexistent(self):
        """Test getting records by non-existent name."""
        db = SimpleDatabase()
        records = db.get_by_name("Nonexistent")
        assert len(records) == 0
    
    def test_get_by_value_range(self):
        """Test getting records by value range."""
        db = SimpleDatabase()
        db.insert("A", 10.0)
        db.insert("B", 20.0)
        db.insert("C", 30.0)
        db.insert("D", 40.0)
        
        records = db.get_by_value_range(15.0, 35.0)
        assert len(records) == 2
        assert all(15.0 <= record.value <= 35.0 for record in records)
    
    def test_delete_by_id_existing(self):
        """Test deleting existing record by ID."""
        db = SimpleDatabase()
        record_id = db.insert("Test", 42.5)
        
        success = db.delete_by_id(record_id)
        assert success
        assert db.record_count() == 0
        assert db.get_by_id(record_id) is None
    
    def test_delete_by_id_nonexistent(self):
        """Test deleting non-existent record by ID."""
        db = SimpleDatabase()
        success = db.delete_by_id(1)
        assert not success
    
    def test_update_by_id_existing(self):
        """Test updating existing record by ID."""
        db = SimpleDatabase()
        record_id = db.insert("Test", 42.5)
        
        success = db.update_by_id(record_id, "Updated", 50.0)
        assert success
        
        record = db.get_by_id(record_id)
        assert record.name == "Updated"
        assert record.value == 50.0
    
    def test_update_by_id_nonexistent(self):
        """Test updating non-existent record by ID."""
        db = SimpleDatabase()
        success = db.update_by_id(1, "Updated", 50.0)
        assert not success
    
    def test_get_all_records(self):
        """Test getting all records."""
        db = SimpleDatabase()
        db.insert("A", 10.0)
        db.insert("B", 20.0)
        db.insert("C", 30.0)
        
        records = db.get_all_records()
        assert len(records) == 3
        assert all(isinstance(record, DatabaseRecord) for record in records)
    
    def test_record_count(self):
        """Test record count."""
        db = SimpleDatabase()
        assert db.record_count() == 0
        
        db.insert("A", 10.0)
        assert db.record_count() == 1
        
        db.insert("B", 20.0)
        assert db.record_count() == 2
    
    def test_clear(self):
        """Test clearing the database."""
        db = SimpleDatabase()
        db.insert("A", 10.0)
        db.insert("B", 20.0)
        
        db.clear()
        assert db.record_count() == 0
        assert db._next_id == 1
    
    def test_get_stats_empty(self):
        """Test getting stats for empty database."""
        db = SimpleDatabase()
        stats = db.get_stats()
        
        assert stats['record_count'] == 0
        assert stats['avg_value'] == 0.0
        assert stats['min_value'] == 0.0
        assert stats['max_value'] == 0.0
    
    def test_get_stats_with_records(self):
        """Test getting stats for database with records."""
        db = SimpleDatabase()
        db.insert("A", 10.0)
        db.insert("B", 20.0)
        db.insert("C", 30.0)
        
        stats = db.get_stats()
        assert stats['record_count'] == 3
        assert stats['avg_value'] == 20.0
        assert stats['min_value'] == 10.0
        assert stats['max_value'] == 30.0
    
    def test_repr(self):
        """Test string representation."""
        db = SimpleDatabase()
        assert repr(db) == "SimpleDatabase(0 records)"
        
        db.insert("Test", 42.5)
        assert repr(db) == "SimpleDatabase(1 records)"


class TestCircularBuffer:
    """Test cases for the CircularBuffer class."""
    
    def test_init_valid_capacity(self):
        """Test initialization with valid capacity."""
        buffer = CircularBuffer(5)
        assert buffer.capacity() == 5
        assert buffer.size() == 0
        assert buffer.is_empty()
        assert not buffer.is_full()
    
    def test_init_invalid_capacity(self):
        """Test initialization with invalid capacity."""
        with pytest.raises(ValueError, match="Capacity must be positive"):
            CircularBuffer(0)
        
        with pytest.raises(ValueError, match="Capacity must be positive"):
            CircularBuffer(-1)
    
    def test_put_and_get(self):
        """Test putting and getting items."""
        buffer = CircularBuffer(3)
        
        buffer.put(1)
        buffer.put(2)
        buffer.put(3)
        
        assert buffer.get() == 1
        assert buffer.get() == 2
        assert buffer.get() == 3
        assert buffer.get() is None  # Buffer is empty
    
    def test_overflow_behavior(self):
        """Test overflow behavior when buffer is full."""
        buffer = CircularBuffer(3)
        
        buffer.put(1)
        buffer.put(2)
        buffer.put(3)
        buffer.put(4)  # This should overwrite 1
        
        assert buffer.get() == 2  # 1 was overwritten
        assert buffer.get() == 3
        assert buffer.get() == 4
        assert buffer.get() is None
    
    def test_peek(self):
        """Test peeking at the oldest item."""
        buffer = CircularBuffer(3)
        
        buffer.put(1)
        buffer.put(2)
        
        assert buffer.peek() == 1
        assert buffer.get() == 1  # Item is still there
        assert buffer.peek() == 2
    
    def test_peek_empty(self):
        """Test peeking at empty buffer."""
        buffer = CircularBuffer(3)
        assert buffer.peek() is None
    
    def test_is_empty(self):
        """Test empty state."""
        buffer = CircularBuffer(3)
        assert buffer.is_empty()
        
        buffer.put(1)
        assert not buffer.is_empty()
        
        buffer.get()
        assert buffer.is_empty()
    
    def test_is_full(self):
        """Test full state."""
        buffer = CircularBuffer(3)
        assert not buffer.is_full()
        
        buffer.put(1)
        buffer.put(2)
        buffer.put(3)
        assert buffer.is_full()
        
        buffer.get()
        assert not buffer.is_full()
    
    def test_size(self):
        """Test size tracking."""
        buffer = CircularBuffer(3)
        assert buffer.size() == 0
        
        buffer.put(1)
        assert buffer.size() == 1
        
        buffer.put(2)
        assert buffer.size() == 2
        
        buffer.put(3)
        assert buffer.size() == 3
        
        buffer.put(4)  # Overflow
        assert buffer.size() == 3  # Size doesn't change on overflow
        
        buffer.get()
        assert buffer.size() == 2
    
    def test_clear(self):
        """Test clearing the buffer."""
        buffer = CircularBuffer(3)
        buffer.put(1)
        buffer.put(2)
        buffer.put(3)
        
        buffer.clear()
        assert buffer.is_empty()
        assert buffer.size() == 0
        assert buffer.get() is None
    
    def test_to_list(self):
        """Test converting buffer to list."""
        buffer = CircularBuffer(3)
        buffer.put(1)
        buffer.put(2)
        buffer.put(3)
        
        items = buffer.to_list()
        assert items == [1, 2, 3]
    
    def test_to_list_with_overflow(self):
        """Test converting buffer to list after overflow."""
        buffer = CircularBuffer(3)
        buffer.put(1)
        buffer.put(2)
        buffer.put(3)
        buffer.put(4)  # Overwrites 1
        
        items = buffer.to_list()
        assert items == [2, 3, 4]
    
    def test_to_list_empty(self):
        """Test converting empty buffer to list."""
        buffer = CircularBuffer(3)
        items = buffer.to_list()
        assert items == []
    
    def test_repr(self):
        """Test string representation."""
        buffer = CircularBuffer(5)
        assert repr(buffer) == "CircularBuffer(size=0, capacity=5)"
        
        buffer.put(1)
        buffer.put(2)
        assert repr(buffer) == "CircularBuffer(size=2, capacity=5)"
    
    def test_complex_usage_pattern(self):
        """Test complex usage pattern with multiple put/get operations."""
        buffer = CircularBuffer(4)
        
        # Fill buffer
        for i in range(4):
            buffer.put(i)
        assert buffer.is_full()
        assert buffer.size() == 4
        
        # Remove some items
        assert buffer.get() == 0
        assert buffer.get() == 1
        assert buffer.size() == 2
        
        # Add more items
        buffer.put(10)
        buffer.put(11)
        assert buffer.size() == 4
        assert buffer.is_full()
        
        # Check remaining items
        assert buffer.get() == 2
        assert buffer.get() == 3
        assert buffer.get() == 10
        assert buffer.get() == 11
        assert buffer.is_empty()


if __name__ == "__main__":
    pytest.main([__file__]) 