"""
Demonstration and benchmarking for Chapter 4: Linked Lists & Iterator Protocol.

This module provides comprehensive demonstrations of the linked list implementations
including performance benchmarks, memory analysis, and real-world usage examples.
"""

import timeit
from typing import List, Dict

from .singly_linked_list import SinglyLinkedList
from .doubly_linked_list import DoublyLinkedList
from .iterator import LinkedListIterator
from .undo_redo import UndoRedoSystem
from .analyzer import LinkedListAnalyzer

def demonstrate_singly_linked_list():
    """Demonstrate the singly linked list implementation."""
    print("=== Singly Linked List Demonstration ===\n")
    
    # Create a singly linked list
    sll = SinglyLinkedList()
    
    # Basic operations
    print("1. Basic Operations:")
    sll.append(10)
    sll.append(20)
    sll.append(30)
    print(f"After append: {sll}")
    
    sll.prepend(5)
    print(f"After prepend: {sll}")
    
    sll.insert_after(20, 25)
    print(f"After insert_after(20, 25): {sll}")
    
    sll.delete_first(20)
    print(f"After delete_first(20): {sll}")
    
    print(f"Length: {len(sll)}")
    print(f"Is empty: {sll.is_empty()}")
    print(f"Contains 25: {sll.contains(25)}")
    print(f"Count of 10: {sll.count(10)}")
    
    # Index operations
    print(f"\n2. Index Operations:")
    print(f"Element at index 1: {sll.get_at_index(1)}")
    sll.set_at_index(1, 15)
    print(f"After set_at_index(1, 15): {sll}")
    
    # Iteration
    print(f"\n3. Iteration:")
    print("Forward iteration:", end=" ")
    for item in sll:
        print(item, end=" ")
    print()
    
    # Reverse
    print(f"\n4. Reverse:")
    print(f"Before reverse: {sll}")
    sll.reverse()
    print(f"After reverse: {sll}")
    
    # Performance test
    print(f"\n5. Performance Test:")
    test_sll = SinglyLinkedList()
    
    # Append performance
    append_time = timeit.timeit(
        lambda: test_sll.append(42),
        number=10000
    )
    print(f"Append 10000 elements: {append_time:.4f} seconds")
    
    # Access performance
    access_time = timeit.timeit(
        lambda: test_sll.get_at_index(5000),
        number=1000
    )
    print(f"Access middle element 1000 times: {access_time:.4f} seconds")

def demonstrate_doubly_linked_list():
    """Demonstrate the doubly linked list implementation."""
    print("\n=== Doubly Linked List Demonstration ===\n")
    
    # Create a doubly linked list
    dll = DoublyLinkedList()
    
    # Basic operations
    print("1. Basic Operations:")
    dll.append(10)
    dll.append(20)
    dll.append(30)
    print(f"After append: {dll}")
    
    dll.prepend(5)
    print(f"After prepend: {dll}")
    
    dll.insert_after(20, 25)
    print(f"After insert_after(20, 25): {dll}")
    
    dll.insert_before(20, 18)
    print(f"After insert_before(20, 18): {dll}")
    
    dll.delete_first(20)
    print(f"After delete_first(20): {dll}")
    
    print(f"Length: {len(dll)}")
    print(f"Is empty: {dll.is_empty()}")
    print(f"Contains 25: {dll.contains(25)}")
    print(f"Count of 10: {dll.count(10)}")
    
    # Index operations with optimization
    print(f"\n2. Index Operations (Optimized):")
    print(f"Element at index 1: {dll.get_at_index(1)}")
    print(f"Element at index 3: {dll.get_at_index(3)}")  # Should use tail traversal
    dll.set_at_index(1, 15)
    print(f"After set_at_index(1, 15): {dll}")
    
    # Bidirectional iteration
    print(f"\n3. Bidirectional Iteration:")
    print("Forward iteration:", end=" ")
    for item in dll:
        print(item, end=" ")
    print()
    
    print("Reverse iteration:", end=" ")
    for item in dll.reverse_iter():
        print(item, end=" ")
    print()
    
    # First/Last operations
    print(f"\n4. First/Last Operations:")
    print(f"First element: {dll.get_first()}")
    print(f"Last element: {dll.get_last()}")
    
    first_removed = dll.remove_first()
    print(f"Removed first ({first_removed}): {dll}")
    
    last_removed = dll.remove_last()
    print(f"Removed last ({last_removed}): {dll}")
    
    # Reverse
    print(f"\n5. Reverse:")
    print(f"Before reverse: {dll}")
    dll.reverse()
    print(f"After reverse: {dll}")
    
    # Performance test
    print(f"\n6. Performance Test:")
    test_dll = DoublyLinkedList()
    
    # Append performance
    append_time = timeit.timeit(
        lambda: test_dll.append(42),
        number=10000
    )
    print(f"Append 10000 elements: {append_time:.4f} seconds")
    
    # Access performance (optimized)
    access_time = timeit.timeit(
        lambda: test_dll.get_at_index(5000),
        number=1000
    )
    print(f"Access middle element 1000 times: {access_time:.4f} seconds")

def demonstrate_advanced_iterator():
    """Demonstrate the advanced iterator implementation."""
    print("\n=== Advanced Iterator Demonstration ===\n")
    
    # Create a doubly linked list for iterator testing
    dll = DoublyLinkedList()
    for i in range(10):
        dll.append(i)
    
    print(f"Original list: {dll}")
    
    # Basic iterator
    print("\n1. Basic Iterator:")
    iterator = LinkedListIterator(dll)
    print("Forward iteration:", end=" ")
    for item in iterator:
        print(item, end=" ")
    print()
    
    # Reverse iterator
    print("\n2. Reverse Iterator:")
    reverse_iterator = LinkedListIterator(dll, direction='reverse')
    print("Reverse iteration:", end=" ")
    for item in reverse_iterator:
        print(item, end=" ")
    print()
    
    # Iterator with start index
    print("\n3. Iterator with Start Index:")
    start_iterator = LinkedListIterator(dll, start_index=3)
    print("Starting from index 3:", end=" ")
    for item in start_iterator:
        print(item, end=" ")
    print()
    
    # Filtering
    print("\n4. Filtering:")
    even_iterator = LinkedListIterator(dll)
    even_numbers = list(even_iterator.filter(lambda x: x % 2 == 0))
    print(f"Even numbers: {even_numbers}")
    
    # Take and skip
    print("\n5. Take and Skip:")
    take_iterator = LinkedListIterator(dll)
    first_three = list(take_iterator.take(3))
    print(f"First three: {first_three}")
    
    skip_iterator = LinkedListIterator(dll)
    after_three = list(skip_iterator.skip(3))
    print(f"After skipping three: {after_three}")
    
    # Mapping
    print("\n6. Mapping:")
    map_iterator = LinkedListIterator(dll)
    doubled = list(map_iterator.map(lambda x: x * 2))
    print(f"Doubled values: {doubled}")
    
    # Enumerate
    print("\n7. Enumerate:")
    enum_iterator = LinkedListIterator(dll)
    enumerated = list(enum_iterator.enumerate())
    print(f"Enumerated: {enumerated}")
    
    # Find and count
    print("\n8. Find and Count:")
    find_iterator = LinkedListIterator(dll)
    first_greater_than_5 = find_iterator.find_first(lambda x: x > 5)
    print(f"First number greater than 5: {first_greater_than_5}")
    
    count_iterator = LinkedListIterator(dll)
    even_count = count_iterator.count_matching(lambda x: x % 2 == 0)
    print(f"Count of even numbers: {even_count}")
    
    # All and any
    print("\n9. All and Any:")
    all_iterator = LinkedListIterator(dll)
    all_positive = all_iterator.all(lambda x: x >= 0)
    print(f"All numbers positive: {all_positive}")
    
    any_iterator = LinkedListIterator(dll)
    any_greater_than_8 = any_iterator.any(lambda x: x > 8)
    print(f"Any number greater than 8: {any_greater_than_8}")

def demonstrate_undo_redo_system():
    """Demonstrate the undo/redo system."""
    print("\n=== Undo/Redo System Demonstration ===\n")
    
    # Create undo/redo system
    undo_redo = UndoRedoSystem()
    
    # Simulate a simple text editor
    text = ""
    
    def add_text(new_text: str):
        nonlocal text
        old_text = text
        text += new_text
        return old_text
    
    def remove_text(old_text: str):
        nonlocal text
        text = old_text
    
    # Execute some actions
    print("1. Executing Actions:")
    undo_redo.execute_action("Add 'Hello'", 
                           lambda: add_text("Hello"), 
                           lambda old: remove_text(old),
                           "Add greeting")
    print(f"Text: '{text}'")
    
    undo_redo.execute_action("Add ' '", 
                           lambda: add_text(" "), 
                           lambda old: remove_text(old),
                           "Add space")
    print(f"Text: '{text}'")
    
    undo_redo.execute_action("Add 'World'", 
                           lambda: add_text("World"), 
                           lambda old: remove_text(old),
                           "Add subject")
    print(f"Text: '{text}'")
    
    undo_redo.execute_action("Add '!'", 
                           lambda: add_text("!"), 
                           lambda old: remove_text(old),
                           "Add exclamation")
    print(f"Text: '{text}'")
    
    print(f"History info: {undo_redo.get_history_info()}")
    
    # Undo operations
    print("\n2. Undoing Actions:")
    while undo_redo.can_undo():
        action_name = undo_redo.undo()
        print(f"Undid: {action_name}, text: '{text}'")
    
    # Redo operations
    print("\n3. Redoing Actions:")
    while undo_redo.can_redo():
        action_name = undo_redo.redo()
        print(f"Redid: {action_name}, text: '{text}'")
    
    # Multiple undo/redo
    print("\n4. Multiple Undo/Redo:")
    undone = undo_redo.undo_multiple(2)
    print(f"Undone multiple actions: {undone}, text: '{text}'")
    
    redone = undo_redo.redo_multiple(1)
    print(f"Redone multiple actions: {redone}, text: '{text}'")
    
    # Performance analysis
    print("\n5. Performance Analysis:")
    
    # Benchmark action execution
    execution_time = timeit.timeit(
        lambda: undo_redo.execute_action("test", lambda: None, lambda x: None),
        number=1000
    )
    print(f"Execute 1000 actions: {execution_time:.4f} seconds")
    
    # Benchmark undo operations
    undo_time = timeit.timeit(
        lambda: undo_redo.undo() if undo_redo.can_undo() else None,
        number=1000
    )
    print(f"Undo 1000 operations: {undo_time:.4f} seconds")

def benchmark_linked_lists():
    """Compare linked list implementations with Python built-ins."""
    print("\n=== Linked List Performance Benchmark ===\n")
    
    # Test data sizes
    sizes = [100, 1000, 10000]
    
    for size in sizes:
        print(f"Testing with {size} elements:")
        print("-" * 50)
        
        # Append operations
        print("Append Operations:")
        
        # Python list append
        list_append = timeit.timeit(
            f"lst.append(i) for i in range({size})",
            setup="lst = []",
            number=1
        )
        
        # Singly linked list append
        singly_append = timeit.timeit(
            f"lst.append(i) for i in range({size})",
            setup="from chapter_04 import SinglyLinkedList; lst = SinglyLinkedList()",
            number=1
        )
        
        # Doubly linked list append
        doubly_append = timeit.timeit(
            f"lst.append(i) for i in range({size})",
            setup="from chapter_04 import DoublyLinkedList; lst = DoublyLinkedList()",
            number=1
        )
        
        print(f"  Python list:      {list_append:.6f} seconds")
        print(f"  Singly linked:    {singly_append:.6f} seconds")
        print(f"  Doubly linked:    {doubly_append:.6f} seconds")
        print()
        
        # Prepend operations
        print("Prepend Operations:")
        
        # Python list insert at beginning
        list_prepend = timeit.timeit(
            f"lst.insert(0, i) for i in range({size})",
            setup="lst = []",
            number=1
        )
        
        # Singly linked list prepend
        singly_prepend = timeit.timeit(
            f"lst.prepend(i) for i in range({size})",
            setup="from chapter_04 import SinglyLinkedList; lst = SinglyLinkedList()",
            number=1
        )
        
        # Doubly linked list prepend
        doubly_prepend = timeit.timeit(
            f"lst.prepend(i) for i in range({size})",
            setup="from chapter_04 import DoublyLinkedList; lst = DoublyLinkedList()",
            number=1
        )
        
        print(f"  Python list:      {list_prepend:.6f} seconds")
        print(f"  Singly linked:    {singly_prepend:.6f} seconds")
        print(f"  Doubly linked:    {doubly_prepend:.6f} seconds")
        print()
        
        # Access operations
        print("Access Operations:")
        
        # Python list access
        list_access = timeit.timeit(
            "lst[500]",
            setup=f"lst = list(range({size}))",
            number=10000
        )
        
        # Singly linked list access
        singly_access = timeit.timeit(
            "lst.get_at_index(500)",
            setup=f"from chapter_04 import SinglyLinkedList; lst = SinglyLinkedList(); [lst.append(i) for i in range({size})]",
            number=10000
        )
        
        # Doubly linked list access
        doubly_access = timeit.timeit(
            "lst.get_at_index(500)",
            setup=f"from chapter_04 import DoublyLinkedList; lst = DoublyLinkedList(); [lst.append(i) for i in range({size})]",
            number=10000
        )
        
        print(f"  Python list:      {list_access:.6f} seconds")
        print(f"  Singly linked:    {singly_access:.6f} seconds")
        print(f"  Doubly linked:    {doubly_access:.6f} seconds")
        print()
        
        # Memory usage comparison
        print("Memory Usage:")
        
        # Python list
        python_list = list(range(size))
        python_memory = sys.getsizeof(python_list)
        
        # Singly linked list
        singly_list = SinglyLinkedList()
        for i in range(size):
            singly_list.append(i)
        singly_memory = LinkedListAnalyzer.analyze_singly_linked_list(singly_list)
        
        # Doubly linked list
        doubly_list = DoublyLinkedList()
        for i in range(size):
            doubly_list.append(i)
        doubly_memory = LinkedListAnalyzer.analyze_doubly_linked_list(doubly_list)
        
        print(f"  Python list:      {python_memory} bytes")
        print(f"  Singly linked:    {singly_memory.total_size} bytes")
        print(f"  Doubly linked:    {doubly_memory.total_size} bytes")
        print()

def demonstrate_memory_analysis():
    """Demonstrate memory analysis capabilities."""
    print("\n=== Memory Analysis Demonstration ===\n")
    
    # Create test lists
    singly_list = SinglyLinkedList()
    doubly_list = DoublyLinkedList()
    
    # Add some data
    test_data = list(range(1000))
    for item in test_data:
        singly_list.append(item)
        doubly_list.append(item)
    
    # Analyze singly linked list
    print("1. Singly Linked List Memory Analysis:")
    singly_analysis = LinkedListAnalyzer.analyze_memory_efficiency(singly_list)
    memory_info = singly_analysis["memory_info"]
    
    print(f"   Object size: {memory_info.object_size} bytes")
    print(f"   Total size: {memory_info.total_size} bytes")
    print(f"   Overhead: {memory_info.overhead} bytes")
    print(f"   Node count: {memory_info.node_count}")
    print(f"   Average node size: {memory_info.average_node_size:.2f} bytes")
    print(f"   Efficiency ratio: {singly_analysis['efficiency_ratio']:.2%}")
    print(f"   Overhead ratio: {singly_analysis['overhead_ratio']:.2%}")
    print(f"   Bytes per element: {singly_analysis['bytes_per_element']:.2f}")
    
    # Analyze doubly linked list
    print("\n2. Doubly Linked List Memory Analysis:")
    doubly_analysis = LinkedListAnalyzer.analyze_memory_efficiency(doubly_list)
    memory_info = doubly_analysis["memory_info"]
    
    print(f"   Object size: {memory_info.object_size} bytes")
    print(f"   Total size: {memory_info.total_size} bytes")
    print(f"   Overhead: {memory_info.overhead} bytes")
    print(f"   Node count: {memory_info.node_count}")
    print(f"   Average node size: {memory_info.average_node_size:.2f} bytes")
    print(f"   Efficiency ratio: {doubly_analysis['efficiency_ratio']:.2%}")
    print(f"   Overhead ratio: {doubly_analysis['overhead_ratio']:.2%}")
    print(f"   Bytes per element: {doubly_analysis['bytes_per_element']:.2f}")
    
    # Comparison
    print("\n3. Memory Comparison:")
    singly_total = singly_analysis["memory_info"].total_size
    doubly_total = doubly_analysis["memory_info"].total_size
    python_total = sys.getsizeof(test_data)
    
    print(f"   Python list: {python_total} bytes")
    print(f"   Singly linked: {singly_total} bytes ({singly_total/python_total:.2f}x)")
    print(f"   Doubly linked: {doubly_total} bytes ({doubly_total/python_total:.2f}x)")
    print(f"   Singly vs Doubly: {doubly_total/singly_total:.2f}x")

def main():
    """Run all demonstrations."""
    print("Chapter 4: Linked Lists & Iterator Protocol")
    print("=" * 50)
    
    try:
        # Run all demonstrations
        demonstrate_singly_linked_list()
        demonstrate_doubly_linked_list()
        demonstrate_advanced_iterator()
        demonstrate_undo_redo_system()
        benchmark_linked_lists()
        demonstrate_memory_analysis()
        
        print("\n" + "=" * 50)
        print("All demonstrations completed successfully!")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 