"""
Configuration Management System

This module provides a practical example of using our custom data structures
in a real-world application - a configuration management system.

Enhanced Features:
- Type validation for configuration values
- Observer pattern for configuration changes
- File persistence (save/load from files)
- Environment variable integration
- Configuration validation and constraints
"""

from typing import Any, Optional, Dict, List, Set, Callable, Type, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import json
import time
import os
from pathlib import Path
from chapter_01.simple_set import SimpleSet
from chapter_01.hash_table import MemoryTrackedHashTable, HashTable
from chapter_01.dynamic_array import DynamicArray, MemoryTrackedDynamicArray

@dataclass
class ConfigItem:
    """A configuration item with metadata and validation."""
    key: str
    value: Any
    description: str = ""
    tags: Set[str] = field(default_factory=set)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    value_type: Optional[Type] = None
    constraints: Dict[str, Any] = field(default_factory=dict)

class ConfigValidator:
    """Validates configuration values based on type and constraints."""
    
    @staticmethod
    def validate_value(value: Any, value_type: Optional[Type] = None, 
                      constraints: Optional[Dict[str, Any]] = None) -> bool:
        """Validate a configuration value."""
        if value_type is not None and not isinstance(value, value_type):
            raise ValueError(f"Value {value} is not of type {value_type}")
        
        if constraints:
            ConfigValidator._check_constraints(value, constraints)
        
        return True
    
    @staticmethod
    def _check_constraints(value: Any, constraints: Dict[str, Any]) -> None:
        """Check value against constraints."""
        if 'min' in constraints and value < constraints['min']:
            raise ValueError(f"Value {value} is less than minimum {constraints['min']}")
        
        if 'max' in constraints and value > constraints['max']:
            raise ValueError(f"Value {value} is greater than maximum {constraints['max']}")
        
        if 'choices' in constraints and value not in constraints['choices']:
            raise ValueError(f"Value {value} not in allowed choices {constraints['choices']}")
        
        if 'pattern' in constraints:
            import re
            if not re.match(constraints['pattern'], str(value)):
                raise ValueError(f"Value {value} does not match pattern {constraints['pattern']}")

class ConfigObserver(ABC):
    """Abstract base class for configuration observers."""
    
    @abstractmethod
    def on_config_changed(self, key: str, old_value: Any, new_value: Any) -> None:
        """Called when a configuration value changes."""
        pass

class ConfigurationManager:
    """
    A configuration management system using our custom data structures.
    
    This demonstrates how our implementations can be used in real-world
    applications, showing their performance characteristics and memory usage.
    
    Enhanced Features:
    - Type validation for configuration values
    - Observer pattern for configuration changes
    - File persistence (save/load from files)
    - Environment variable integration
    - Configuration validation and constraints
    """
    
    def __init__(self, config_file: Optional[str] = None):
        from chapter_01.hash_table import HashTable
        from chapter_01.dynamic_array import DynamicArray, MemoryTrackedDynamicArray
        
        self._configs = MemoryTrackedHashTable[str, ConfigItem]()
        self._tags = MemoryTrackedHashTable[str, SimpleSet[str]]()
        self._history = MemoryTrackedDynamicArray[Dict[str, Any]]()
        self._observers: List[ConfigObserver] = []
        self._config_file = config_file
        
        # Load from file if specified
        if config_file and Path(config_file).exists():
            self.load_from_file(config_file)
    
    def add_observer(self, observer: ConfigObserver) -> None:
        """Add a configuration change observer."""
        self._observers.append(observer)
    
    def remove_observer(self, observer: ConfigObserver) -> None:
        """Remove a configuration change observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self, key: str, old_value: Any, new_value: Any) -> None:
        """Notify all observers of a configuration change."""
        for observer in self._observers:
            observer.on_config_changed(key, old_value, new_value)
    
    def set_config(self, key: str, value: Any, description: str = "", 
                  tags: Set[str] = None, value_type: Optional[Type] = None,
                  constraints: Optional[Dict[str, Any]] = None) -> None:
        """
        Set a configuration value with validation.
        
        Args:
            key: Configuration key
            value: Configuration value
            description: Optional description
            tags: Optional tags for categorization
            value_type: Expected type for validation
            constraints: Validation constraints (min, max, choices, pattern)
        """
        if tags is None:
            tags = set()
        
        # Validate value
        ConfigValidator.validate_value(value, value_type, constraints)
        
        # Get old value for observer notification
        old_value = None
        if key in self._configs:
            old_value = self._configs[key].value
        
        # Create config item
        config_item = ConfigItem(
            key=key,
            value=value,
            description=description,
            tags=tags.copy(),
            value_type=value_type,
            constraints=constraints or {}
        )
        
        # Store in main config table
        self._configs[key] = config_item
        
        # Update tag index
        for tag in tags:
            if tag not in self._tags:
                self._tags[tag] = SimpleSet[str]()
            self._tags[tag].add(key)
        
        # Add to history
        self._history.append({
            "action": "set",
            "key": key,
            "value": value,
            "timestamp": time.time()
        })
        
        # Notify observers
        self._notify_observers(key, old_value, value)
    
    def get_config(self, key: str, default: Any = None) -> Optional[Any]:
        """Get a configuration value with optional default."""
        if key in self._configs:
            return self._configs[key].value
        return default
    
    def get_config_with_metadata(self, key: str) -> Optional[ConfigItem]:
        """Get a configuration item with full metadata."""
        return self._configs.get(key)
    
    def delete_config(self, key: str) -> bool:
        """Delete a configuration value."""
        if key not in self._configs:
            return False
        
        config_item = self._configs[key]
        old_value = config_item.value
        
        # Remove from tag index
        for tag in config_item.tags:
            if tag in self._tags:
                self._tags[tag].discard(key)
                if len(self._tags[tag]) == 0:
                    del self._tags[tag]
        
        # Remove from main config
        del self._configs[key]
        
        # Add to history
        self._history.append({
            "action": "delete",
            "key": key,
            "timestamp": time.time()
        })
        
        # Notify observers
        self._notify_observers(key, old_value, None)
        
        return True
    
    def get_by_tag(self, tag: str) -> List[str]:
        """Get all config keys with a specific tag."""
        if tag in self._tags:
            return list(self._tags[tag])
        return []
    
    def search_configs(self, query: str) -> List[str]:
        """Search configs by key or description."""
        results = []
        query_lower = query.lower()
        
        for key, config in self._configs.items():
            if (query_lower in key.lower() or 
                query_lower in config.description.lower()):
                results.append(key)
        
        return results
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent configuration history."""
        start = max(0, len(self._history) - limit)
        return list(self._history)[start:]
    
    def export_json(self) -> str:
        """Export configuration to JSON."""
        config_data = {}
        for key, config in self._configs.items():
            config_data[key] = {
                "value": config.value,
                "description": config.description,
                "tags": list(config.tags),
                "created_at": config.created_at,
                "updated_at": config.updated_at,
                "value_type": config.value_type.__name__ if config.value_type else None,
                "constraints": config.constraints
            }
        
        return json.dumps(config_data, indent=2)
    
    def import_json(self, json_data: str) -> None:
        """Import configuration from JSON."""
        config_data = json.loads(json_data)
        
        for key, data in config_data.items():
            # Convert type name back to type object
            value_type = None
            if data.get("value_type"):
                value_type = globals().get(data["value_type"])
            
            self.set_config(
                key=key,
                value=data["value"],
                description=data.get("description", ""),
                tags=set(data.get("tags", [])),
                value_type=value_type,
                constraints=data.get("constraints", {})
            )
    
    def save_to_file(self, filename: Optional[str] = None) -> None:
        """Save configuration to a file."""
        if filename is None:
            filename = self._config_file
        
        if filename is None:
            raise ValueError("No filename specified for saving")
        
        with open(filename, 'w') as f:
            f.write(self.export_json())
    
    def load_from_file(self, filename: str) -> None:
        """Load configuration from a file."""
        with open(filename, 'r') as f:
            json_data = f.read()
        self.import_json(json_data)
    
    def load_from_environment(self, prefix: str = "APP_") -> None:
        """
        Load configuration from environment variables.
        
        Args:
            prefix: Prefix for environment variables to load
        """
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower()
                
                # Try to infer type
                try:
                    # Try as int
                    typed_value = int(value)
                except ValueError:
                    try:
                        # Try as float
                        typed_value = float(value)
                    except ValueError:
                        # Keep as string
                        typed_value = value
                
                self.set_config(
                    key=config_key,
                    value=typed_value,
                    description=f"Loaded from environment variable {key}",
                    tags={"environment", "auto-loaded"}
                )
    
    def validate_all_configs(self) -> Dict[str, List[str]]:
        """Validate all configuration values and return any errors."""
        errors = {}
        
        for key, config in self._configs.items():
            try:
                ConfigValidator.validate_value(
                    config.value, 
                    config.value_type, 
                    config.constraints
                )
            except ValueError as e:
                errors[key] = [str(e)]
        
        return errors
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory usage statistics."""
        config_info = self._configs.get_memory_info()
        tag_info = self._tags.get_memory_info()
        history_info = self._history.get_memory_info()
        
        return {
            "configs": {
                "size": len(self._configs),
                "memory": config_info.object_size,
                "load_factor": config_info.load_factor
            },
            "tags": {
                "size": len(self._tags),
                "memory": tag_info.object_size,
                "load_factor": tag_info.load_factor
            },
            "history": {
                "size": len(self._history),
                "memory": history_info.object_size,
                "load_factor": history_info.load_factor
            },
            "observers": {
                "count": len(self._observers)
            },
            "total_memory": config_info.object_size + tag_info.object_size + history_info.object_size
        }

# Example observer implementation
class LoggingConfigObserver(ConfigObserver):
    """Observer that logs configuration changes."""
    
    def on_config_changed(self, key: str, old_value: Any, new_value: Any) -> None:
        """Log configuration changes."""
        print(f"Config changed: {key} = {old_value} -> {new_value}")

class ValidationConfigObserver(ConfigObserver):
    """Observer that validates configuration changes."""
    
    def on_config_changed(self, key: str, old_value: Any, new_value: Any) -> None:
        """Validate configuration changes."""
        if new_value is not None:
            print(f"Validating config change: {key} = {new_value}")
            # Add custom validation logic here 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running config_manager demonstration...")
    print("=" * 50)

    # Create instance of ConfigItem
    try:
        instance = ConfigItem()
        print(f"✓ Created ConfigItem instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating ConfigItem instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
