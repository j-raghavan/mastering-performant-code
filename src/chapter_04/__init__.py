"""
Chapter 4: Linked Lists & Iterator Protocol

This module provides implementations of singly and doubly linked lists
with proper iterator protocol, sentinel nodes, and advanced features.

Classes:
    - SinglyNode: Node for singly linked list
    - DoublyNode: Node for doubly linked list
    - SinglyLinkedList: Singly linked list implementation
    - DoublyLinkedList: Doubly linked list implementation
    - LinkedListIterator: Advanced iterator with additional features
    - UndoRedoSystem: Real-world application using linked lists
    - LinkedListAnalyzer: Memory and performance analysis tools
"""

from .nodes import SinglyNode, DoublyNode
from .singly_linked_list import SinglyLinkedList
from .doubly_linked_list import DoublyLinkedList
from .iterator import LinkedListIterator, IteratorState
from .undo_redo import UndoRedoSystem, Action
from .analyzer import LinkedListAnalyzer, MemoryInfo

__all__ = [
    'SinglyNode',
    'DoublyNode', 
    'SinglyLinkedList',
    'DoublyLinkedList',
    'LinkedListIterator',
    'IteratorState',
    'UndoRedoSystem',
    'Action',
    'LinkedListAnalyzer',
    'MemoryInfo'
] 