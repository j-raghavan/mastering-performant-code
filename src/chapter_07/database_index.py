"""
Database Index Implementation using AVL Trees

This module demonstrates how AVL trees can be used in real-world applications
for efficient data retrieval and range queries.
"""

from typing import Dict, List, Optional, Tuple, Any
import json
from .avl_tree import AVLTree, AVLNode

class DatabaseIndex:
    """
    A simple database index implementation using AVL trees.
    
    This demonstrates how AVL trees can be used in real-world applications
    for efficient data retrieval and range queries.
    """
    
    def __init__(self):
        self._index: AVLTree[Tuple[str, Any, int]] = AVLTree()
        self._data: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1
    
    def insert_record(self, record: Dict[str, Any]) -> int:
        """Insert a record and update the index."""
        record_id = self._next_id
        self._next_id += 1
        
        # Store the record
        self._data[record_id] = record.copy()
        
        # Update index for each searchable field
        for field_name, field_value in record.items():
            if isinstance(field_value, (str, int, float)):
                index_key = (field_name, field_value, record_id)
                self._index.insert(index_key)
        
        return record_id
    
    def search_by_field(self, field_name: str, field_value: Any) -> List[Dict[str, Any]]:
        """Search for records by a specific field value."""
        results = []
        
        # Traverse all index entries and find matches
        for index_key in self._index.inorder_traversal():
            node_field, node_value, node_id = index_key
            
            if node_field == field_name and node_value == field_value:
                if node_id in self._data:
                    results.append(self._data[node_id])
        
        return results
    
    def range_query(self, field_name: str, min_value: Any, max_value: Any) -> List[Dict[str, Any]]:
        """Search for records within a range of field values."""
        results = []
        
        # Traverse all index entries and find matches
        for index_key in self._index.inorder_traversal():
            node_field, node_value, node_id = index_key
            
            if node_field == field_name and min_value <= node_value <= max_value:
                if node_id in self._data:
                    results.append(self._data[node_id])
        
        return results
    
    def delete_record(self, record_id: int) -> bool:
        """Delete a record and update the index."""
        if record_id not in self._data:
            return False
        
        record = self._data[record_id]
        
        # Remove index entries
        for field_name, field_value in record.items():
            if isinstance(field_value, (str, int, float)):
                index_key = (field_name, field_value, record_id)
                self._index.delete(index_key)
        
        # Remove the record
        del self._data[record_id]
        return True
    
    def get_all_records(self) -> List[Dict[str, Any]]:
        """Get all records in the database."""
        return list(self._data.values())
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get statistics about the index."""
        return {
            'total_records': len(self._data),
            'index_size': len(self._index),
            'index_height': self._index.height(),
            'is_balanced': self._index.is_balanced()
        }
    
    def export_to_json(self, filename: str) -> None:
        """Export the database to a JSON file."""
        data = {
            'records': self._data,
            'next_id': self._next_id
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def import_from_json(self, filename: str) -> None:
        """Import the database from a JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Convert string keys back to integers
        self._data = {int(k): v for k, v in data['records'].items()}
        self._next_id = data['next_id']
        
        # Rebuild index
        self._index = AVLTree()
        for record_id, record in self._data.items():
            for field_name, field_value in record.items():
                if isinstance(field_value, (str, int, float)):
                    index_key = (field_name, field_value, record_id)
                    self._index.insert(index_key)
    
    def get_field_values(self, field_name: str) -> List[Any]:
        """Get all unique values for a specific field."""
        values = set()
        
        # Traverse all index entries and collect values for the field
        for index_key in self._index.inorder_traversal():
            node_field, node_value, _ = index_key
            
            if node_field == field_name:
                values.add(node_value)
        
        return sorted(list(values))
    
    def get_field_statistics(self, field_name: str) -> Dict[str, Any]:
        """Get statistics for a specific field."""
        values = self.get_field_values(field_name)
        
        if not values:
            return {
                'field_name': field_name,
                'count': 0,
                'min': None,
                'max': None,
                'unique_values': 0
            }
        
        # Count total records with this field
        total_count = 0
        for record in self._data.values():
            if field_name in record:
                total_count += 1
        
        numeric_values = [v for v in values if isinstance(v, (int, float))]
        
        stats = {
            'field_name': field_name,
            'count': total_count,
            'unique_values': len(set(values)),
            'min': min(values) if values else None,
            'max': max(values) if values else None
        }
        
        if numeric_values:
            stats['numeric_min'] = min(numeric_values)
            stats['numeric_max'] = max(numeric_values)
            # Count total records with a numeric value for this field
            numeric_count = 0
            for record in self._data.values():
                v = record.get(field_name, None)
                if isinstance(v, (int, float)):
                    numeric_count += 1
            stats['numeric_count'] = numeric_count
        
        return stats 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running database_index demonstration...")
    print("=" * 50)

    # Create instance of DatabaseIndex
    try:
        instance = DatabaseIndex()
        print(f"✓ Created DatabaseIndex instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating DatabaseIndex instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
