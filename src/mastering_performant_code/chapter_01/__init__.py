"""
Chapter 1: Built-ins Under the Hood - list, dict, set

This module contains implementations of Python's built-in data structures
to demonstrate their internal workings and performance characteristics.
"""

from .dynamic_array import DynamicArray, MemoryTrackedDynamicArray
from .hash_table import HashTable, MemoryTrackedHashTable
from .simple_set import SimpleSet
from .analyzer import BuiltinAnalyzer, MemoryInfo
from .config_manager import ConfigurationManager, ConfigItem

__all__ = [
    'DynamicArray',
    'MemoryTrackedDynamicArray', 
    'HashTable',
    'MemoryTrackedHashTable',
    'SimpleSet',
    'BuiltinAnalyzer',
    'MemoryInfo',
    'ConfigurationManager',
    'ConfigItem'
] 