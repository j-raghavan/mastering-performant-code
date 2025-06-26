"""
Real-World Applications of Dynamic Arrays

This module contains practical applications that demonstrate how dynamic arrays
are used in real-world scenarios like text editors and databases.
"""

from typing import Optional, List
from .dynamic_array import ProductionDynamicArray


class TextBuffer:
    """
    A simple text editor buffer using dynamic arrays.
    
    This demonstrates how dynamic arrays are used in real applications
    like text editors, where efficient insertion and deletion are crucial.
    """
    
    def __init__(self):
        self._lines = ProductionDynamicArray[str]()
        self._cursor_line = 0
        self._cursor_col = 0
    
    def insert_line(self, line_num: int, text: str) -> None:
        """Insert a new line at the specified position."""
        if not 0 <= line_num <= len(self._lines):
            raise IndexError(f"Line number {line_num} out of range")
        
        self._lines.insert(line_num, text)
        if line_num <= self._cursor_line:
            self._cursor_line += 1
    
    def delete_line(self, line_num: int) -> str:
        """Delete and return the line at the specified position."""
        if not 0 <= line_num < len(self._lines):
            raise IndexError(f"Line number {line_num} out of range")
        
        if line_num == self._cursor_line:
            self._cursor_line = max(0, self._cursor_line - 1)
        elif line_num < self._cursor_line:
            self._cursor_line -= 1
        
        return self._lines.pop(line_num)
    
    def get_line(self, line_num: int) -> str:
        """Get the line at the specified position."""
        if not 0 <= line_num < len(self._lines):
            raise IndexError(f"Line number {line_num} out of range")
        return self._lines[line_num]
    
    def set_line(self, line_num: int, text: str) -> None:
        """Set the content of a line at the specified position."""
        if not 0 <= line_num < len(self._lines):
            raise IndexError(f"Line number {line_num} out of range")
        self._lines[line_num] = text
    
    def get_all_lines(self) -> List[str]:
        """Get all lines as a list."""
        return list(self._lines)
    
    def line_count(self) -> int:
        """Get the number of lines."""
        return len(self._lines)
    
    def append_line(self, text: str) -> None:
        """Add a new line at the end."""
        self._lines.append(text)
    
    def insert_text(self, line_num: int, col: int, text: str) -> None:
        """Insert text at a specific position in a line."""
        if not 0 <= line_num < len(self._lines):
            raise IndexError(f"Line number {line_num} out of range")
        
        current_line = self._lines[line_num]
        if not 0 <= col <= len(current_line):
            raise IndexError(f"Column {col} out of range for line {line_num}")
        
        new_line = current_line[:col] + text + current_line[col:]
        self._lines[line_num] = new_line
    
    def delete_text(self, line_num: int, start_col: int, end_col: int) -> str:
        """Delete text from a line and return the deleted text."""
        if not 0 <= line_num < len(self._lines):
            raise IndexError(f"Line number {line_num} out of range")
        
        current_line = self._lines[line_num]
        if not 0 <= start_col <= end_col <= len(current_line):
            raise IndexError(f"Invalid column range: {start_col}-{end_col}")
        
        deleted_text = current_line[start_col:end_col]
        new_line = current_line[:start_col] + current_line[end_col:]
        self._lines[line_num] = new_line
        
        return deleted_text
    
    def set_cursor(self, line: int, col: int) -> None:
        """Set the cursor position."""
        # Allow setting cursor at line 0, column 0 even when there are no lines
        if line == 0 and col == 0 and len(self._lines) == 0:
            self._cursor_line = line
            self._cursor_col = col
            return
        
        if not 0 <= line < len(self._lines):
            raise IndexError(f"Line number {line} out of range")
        
        # Allow setting cursor at column 0 even for empty lines
        if line < len(self._lines) and col > len(self._lines[line]):
            raise IndexError(f"Column {col} out of range for line {line}")
        
        self._cursor_line = line
        self._cursor_col = col
    
    def get_cursor_position(self) -> tuple[int, int]:
        """Get the current cursor position."""
        return (self._cursor_line, self._cursor_col)
    
    def __repr__(self) -> str:
        return f"TextBuffer({self.line_count()} lines, cursor at {self.get_cursor_position()})"


class DatabaseRecord:
    """A simple database record."""
    
    def __init__(self, id: int, name: str, value: float):
        self.id = id
        self.name = name
        self.value = value
    
    def __repr__(self) -> str:
        return f"Record(id={self.id}, name='{self.name}', value={self.value})"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DatabaseRecord):
            return False
        return (self.id == other.id and 
                self.name == other.name and 
                self.value == other.value)
    
    def __hash__(self) -> int:
        return hash((self.id, self.name, self.value))


class SimpleDatabase:
    """
    A simple in-memory database using dynamic arrays.
    
    This demonstrates how dynamic arrays can be used for record storage
    in database systems.
    """
    
    def __init__(self):
        self._records = ProductionDynamicArray[DatabaseRecord]()
        self._next_id = 1
    
    def insert(self, name: str, value: float) -> int:
        """Insert a new record and return its ID."""
        record = DatabaseRecord(self._next_id, name, value)
        self._records.append(record)
        self._next_id += 1
        return record.id
    
    def get_by_id(self, id: int) -> Optional[DatabaseRecord]:
        """Get a record by ID."""
        for record in self._records:
            if record.id == id:
                return record
        return None
    
    def get_by_name(self, name: str) -> List[DatabaseRecord]:
        """Get all records with the given name."""
        result = []
        for record in self._records:
            if record.name == name:
                result.append(record)
        return result
    
    def get_by_value_range(self, min_value: float, max_value: float) -> List[DatabaseRecord]:
        """Get all records with values in the specified range."""
        result = []
        for record in self._records:
            if min_value <= record.value <= max_value:
                result.append(record)
        return result
    
    def delete_by_id(self, id: int) -> bool:
        """Delete a record by ID."""
        for i, record in enumerate(self._records):
            if record.id == id:
                self._records.pop(i)
                return True
        return False
    
    def update_by_id(self, id: int, name: str, value: float) -> bool:
        """Update a record by ID."""
        for record in self._records:
            if record.id == id:
                record.name = name
                record.value = value
                return True
        return False
    
    def get_all_records(self) -> List[DatabaseRecord]:
        """Get all records."""
        return list(self._records)
    
    def record_count(self) -> int:
        """Get the number of records."""
        return len(self._records)
    
    def clear(self) -> None:
        """Clear all records."""
        self._records.clear()
        self._next_id = 1
    
    def get_stats(self) -> dict:
        """Get database statistics."""
        if self.record_count() == 0:
            return {
                'record_count': 0,
                'avg_value': 0.0,
                'min_value': 0.0,
                'max_value': 0.0
            }
        
        values = [record.value for record in self._records]
        return {
            'record_count': self.record_count(),
            'avg_value': sum(values) / len(values),
            'min_value': min(values),
            'max_value': max(values)
        }
    
    def __repr__(self) -> str:
        return f"SimpleDatabase({self.record_count()} records)"


class CircularBuffer:
    """
    A circular buffer implementation using dynamic arrays.
    
    A circular buffer is a fixed-size buffer that overwrites the oldest
    data when full. This is useful for streaming data, audio processing,
    and other applications where you need a sliding window of recent data.
    """
    
    def __init__(self, capacity: int):
        """Initialize a circular buffer with the specified capacity."""
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        
        self._capacity = capacity
        self._buffer = ProductionDynamicArray[Optional[object]]()
        self._head = 0  # Index of the oldest element
        self._tail = 0  # Index of the next position to write
        self._size = 0  # Number of elements currently in the buffer
        
        # Initialize buffer with None values
        for _ in range(capacity):
            self._buffer.append(None)
    
    def put(self, item: object) -> None:
        """Add an item to the buffer, overwriting the oldest if full."""
        self._buffer[self._tail] = item
        
        if self._size < self._capacity:
            self._size += 1
        else:
            # Buffer is full, move head to next position
            self._head = (self._head + 1) % self._capacity
        
        # Move tail to next position
        self._tail = (self._tail + 1) % self._capacity
    
    def get(self) -> Optional[object]:
        """Get and remove the oldest item from the buffer."""
        if self._size == 0:
            return None
        
        item = self._buffer[self._head]
        self._head = (self._head + 1) % self._capacity
        self._size -= 1
        
        return item
    
    def peek(self) -> Optional[object]:
        """Get the oldest item without removing it."""
        if self._size == 0:
            return None
        return self._buffer[self._head]
    
    def is_empty(self) -> bool:
        """Check if the buffer is empty."""
        return self._size == 0
    
    def is_full(self) -> bool:
        """Check if the buffer is full."""
        return self._size == self._capacity
    
    def size(self) -> int:
        """Get the number of elements currently in the buffer."""
        return self._size
    
    def capacity(self) -> int:
        """Get the capacity of the buffer."""
        return self._capacity
    
    def clear(self) -> None:
        """Clear all elements from the buffer."""
        self._head = 0
        self._tail = 0
        self._size = 0
    
    def to_list(self) -> List[object]:
        """Convert the buffer to a list in order (oldest first)."""
        result = []
        for i in range(self._size):
            index = (self._head + i) % self._capacity
            result.append(self._buffer[index])
        return result
    
    def __repr__(self) -> str:
        return f"CircularBuffer(size={self._size}, capacity={self._capacity})" 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running applications demonstration...")
    print("=" * 50)

    # Create instance of TextBuffer
    try:
        instance = TextBuffer()
        print(f"✓ Created TextBuffer instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating TextBuffer instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
