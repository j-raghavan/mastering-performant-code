"""
AVL Tree Demo and Interactive Testing

This module provides a comprehensive demo that showcases all AVL tree features
including insertion, deletion, traversal, and performance benchmarking.
"""

import timeit
from typing import List
from .avl_tree import AVLTree
from .analyzer import AVLTreeAnalyzer
from .database_index import DatabaseIndex

def visualize_tree_structure(tree: AVLTree) -> str:
    """Create ASCII visualization of tree structure."""
    if tree.is_empty():
        return "Empty Tree"
    
    def get_node_info(node):
        """Get node information for display."""
        if node is None:
            return "None"
        bf = node.get_balance_factor()
        return f"{node.value}(h={node.height},bf={bf})"
    
    def build_levels(node, level=0, levels=None):
        """Build tree levels for visualization."""
        if levels is None:
            levels = []
        
        if len(levels) <= level:
            levels.append([])
        
        if node is None:
            levels[level].append("None")
        else:
            levels[level].append(get_node_info(node))
            build_levels(node.left, level + 1, levels)
            build_levels(node.right, level + 1, levels)
        
        return levels
    
    levels = build_levels(tree._root)
    
    # Build visualization string
    result = []
    for i, level in enumerate(levels):
        if any(node != "None" for node in level):
            indent = "  " * (len(levels) - i - 1)
            level_str = indent + "  ".join(level)
            result.append(f"Level {i}: {level_str}")
    
    return "\n".join(result)

def run_avl_tree_demo():
    """Run an interactive demo of the AVL tree implementation."""
    print("AVL Tree Implementation Demo")
    print("=" * 50)
    
    # Create AVL tree
    avl_tree = AVLTree()
    
    # Insert some values
    print("\n1. Inserting values: [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]")
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45, 55, 65, 75, 85]
    
    for value in values:
        avl_tree.insert(value)
        print(f"Inserted {value}, Tree height: {avl_tree.height()}, Balanced: {avl_tree.is_balanced()}")
    
    print(f"\nFinal tree size: {len(avl_tree)}")
    print(f"Final tree height: {avl_tree.height()}")
    print(f"Is balanced: {avl_tree.is_balanced()}")
    
    # Traversal demonstrations
    print("\n2. Tree Traversals:")
    print(f"Inorder: {list(avl_tree.inorder_traversal())}")
    print(f"Preorder: {list(avl_tree.preorder_traversal())}")
    print(f"Postorder: {list(avl_tree.postorder_traversal())}")
    
    print("\nLevel-order traversal:")
    for level, values in enumerate(avl_tree.level_order_traversal()):
        print(f"Level {level}: {values}")
    
    # Tree visualization
    print("\n2.5. Tree Structure Visualization:")
    print(visualize_tree_structure(avl_tree))
    
    # Search demonstrations
    print("\n3. Search Operations:")
    search_values = [50, 25, 90, 35]
    for value in search_values:
        result = avl_tree.search(value)
        if result:
            print(f"Found {value} in tree")
        else:
            print(f"{value} not found in tree")
    
    # Successor and predecessor
    print("\n4. Successor and Predecessor:")
    test_values = [25, 50, 75]
    for value in test_values:
        successor = avl_tree.successor(value)
        predecessor = avl_tree.predecessor(value)
        print(f"Value: {value}, Successor: {successor}, Predecessor: {predecessor}")
    
    # Deletion demonstration
    print("\n5. Deletion Operations:")
    delete_values = [30, 50, 70]
    for value in delete_values:
        print(f"\nDeleting {value}...")
        avl_tree.delete(value)
        print(f"Tree size: {len(avl_tree)}, Height: {avl_tree.height()}, Balanced: {avl_tree.is_balanced()}")
        print(f"Remaining values: {avl_tree.get_sorted_values()}")
    
    # Performance benchmarking
    print("\n6. Performance Benchmarking:")
    analyzer = AVLTreeAnalyzer()
    
    data_sizes = [100, 1000, 10000]
    insertion_results = analyzer.benchmark_insertion(data_sizes, num_trials=3)
    analyzer.print_benchmark_results(insertion_results, "Insertion Performance (seconds)")
    
    search_results = analyzer.benchmark_search(data_sizes, num_trials=3)
    analyzer.print_benchmark_results(search_results, "Search Performance (seconds)")
    
    # Tree properties analysis
    print("\n7. Tree Properties Analysis:")
    tree_analysis = analyzer.analyze_tree_properties(data_sizes)
    analyzer.print_tree_analysis(tree_analysis)
    
    # Rotation benchmarks
    print("\n8. Rotation Performance Analysis:")
    rotation_results = analyzer.benchmark_rotation_scenarios(num_trials=5)
    analyzer.print_rotation_benchmarks(rotation_results)
    
    # Memory usage analysis
    print("\n8.5. Memory Usage Analysis:")
    memory_results = analyzer.benchmark_memory_usage([100, 1000, 10000])
    analyzer.print_memory_analysis(memory_results)
    
    # Fibonacci height analysis
    print("\n8.6. Fibonacci Height Analysis:")
    for size in [100, 1000, 10000]:
        analysis = analyzer.fibonacci_avl_height_analysis(size)
        print(f"Size {size}: Min height={analysis['min_height']}, "
              f"AVL bound={analysis['avl_height_bound']}, "
              f"Efficiency={analysis['height_efficiency']:.3f}")
    
    # Database index demonstration
    print("\n9. Database Index Application:")
    db_index = DatabaseIndex()
    
    # Insert some sample records
    records = [
        {"name": "Alice", "age": 25, "city": "New York"},
        {"name": "Bob", "age": 30, "city": "Los Angeles"},
        {"name": "Charlie", "age": 35, "city": "Chicago"},
        {"name": "Diana", "age": 28, "city": "New York"},
        {"name": "Eve", "age": 32, "city": "Boston"}
    ]
    
    for record in records:
        record_id = db_index.insert_record(record)
        print(f"Inserted record {record_id}: {record}")
    
    print(f"\nDatabase stats: {db_index.get_index_stats()}")
    
    # Search demonstrations
    print("\nSearching for people in New York:")
    ny_people = db_index.search_by_field("city", "New York")
    for person in ny_people:
        print(f"  {person}")
    
    print("\nSearching for people aged 25-30:")
    young_people = db_index.range_query("age", 25, 30)
    for person in young_people:
        print(f"  {person}")
    
    # Field statistics
    print("\nField Statistics:")
    age_stats = db_index.get_field_statistics("age")
    print(f"Age statistics: {age_stats}")
    
    city_stats = db_index.get_field_statistics("city")
    print(f"City statistics: {city_stats}")
    
    print("\nDemo completed!")

def demonstrate_rotation_scenarios():
    """Demonstrate different rotation scenarios in AVL trees."""
    print("\nAVL Tree Rotation Scenarios Demo")
    print("=" * 40)
    
    # Left-Left rotation scenario
    print("\n1. Left-Left Rotation Scenario:")
    print("Inserting: [30, 20, 10]")
    avl_ll = AVLTree()
    values_ll = [30, 20, 10]
    for value in values_ll:
        avl_ll.insert(value)
        print(f"After inserting {value}: Height={avl_ll.height()}, Balanced={avl_ll.is_balanced()}")
    print(f"Final tree: {list(avl_ll.inorder_traversal())}")
    
    # Right-Right rotation scenario
    print("\n2. Right-Right Rotation Scenario:")
    print("Inserting: [10, 20, 30]")
    avl_rr = AVLTree()
    values_rr = [10, 20, 30]
    for value in values_rr:
        avl_rr.insert(value)
        print(f"After inserting {value}: Height={avl_rr.height()}, Balanced={avl_rr.is_balanced()}")
    print(f"Final tree: {list(avl_rr.inorder_traversal())}")
    
    # Left-Right rotation scenario
    print("\n3. Left-Right Rotation Scenario:")
    print("Inserting: [30, 10, 20]")
    avl_lr = AVLTree()
    values_lr = [30, 10, 20]
    for value in values_lr:
        avl_lr.insert(value)
        print(f"After inserting {value}: Height={avl_lr.height()}, Balanced={avl_lr.is_balanced()}")
    print(f"Final tree: {list(avl_lr.inorder_traversal())}")
    
    # Right-Left rotation scenario
    print("\n4. Right-Left Rotation Scenario:")
    print("Inserting: [10, 30, 20]")
    avl_rl = AVLTree()
    values_rl = [10, 30, 20]
    for value in values_rl:
        avl_rl.insert(value)
        print(f"After inserting {value}: Height={avl_rl.height()}, Balanced={avl_rl.is_balanced()}")
    print(f"Final tree: {list(avl_rl.inorder_traversal())}")

def benchmark_comparison():
    """Compare AVL tree performance with other data structures."""
    print("\nPerformance Comparison Benchmark")
    print("=" * 40)
    
    analyzer = AVLTreeAnalyzer()
    
    # Small dataset comparison
    print("\nSmall Dataset (1000 elements):")
    small_results = analyzer.benchmark_insertion([1000], num_trials=5)
    print(f"AVL Tree: {small_results['avl_tree'][0]:.6f} seconds")
    print(f"Set: {small_results['set'][0]:.6f} seconds")
    print(f"List: {small_results['list'][0]:.6f} seconds")
    
    # Medium dataset comparison
    print("\nMedium Dataset (10000 elements):")
    medium_results = analyzer.benchmark_insertion([10000], num_trials=3)
    print(f"AVL Tree: {medium_results['avl_tree'][0]:.6f} seconds")
    print(f"Set: {medium_results['set'][0]:.6f} seconds")
    print(f"List: {medium_results['list'][0]:.6f} seconds")
    
    # Search performance comparison
    print("\nSearch Performance (10000 elements):")
    search_results = analyzer.benchmark_search([10000], num_trials=3)
    print(f"AVL Tree: {search_results['avl_tree'][0]:.6f} seconds")
    print(f"Set: {search_results['set'][0]:.6f} seconds")
    print(f"List: {search_results['list'][0]:.6f} seconds")

def demonstrate_database_features():
    """Demonstrate advanced database index features."""
    print("\nAdvanced Database Index Features")
    print("=" * 40)
    
    db_index = DatabaseIndex()
    
    # Insert a larger dataset
    records = [
        {"name": "Alice", "age": 25, "city": "New York", "salary": 75000},
        {"name": "Bob", "age": 30, "city": "Los Angeles", "salary": 85000},
        {"name": "Charlie", "age": 35, "city": "Chicago", "salary": 90000},
        {"name": "Diana", "age": 28, "city": "New York", "salary": 80000},
        {"name": "Eve", "age": 32, "city": "Boston", "salary": 95000},
        {"name": "Frank", "age": 27, "city": "San Francisco", "salary": 100000},
        {"name": "Grace", "age": 29, "city": "Seattle", "salary": 88000},
        {"name": "Henry", "age": 31, "city": "Austin", "salary": 92000}
    ]
    
    for record in records:
        record_id = db_index.insert_record(record)
        print(f"Inserted: {record['name']} (ID: {record_id})")
    
    print(f"\nDatabase Statistics: {db_index.get_index_stats()}")
    
    # Complex queries
    print("\nComplex Queries:")
    
    # Range query on age
    print("People aged 25-30:")
    young_people = db_index.range_query("age", 25, 30)
    for person in young_people:
        print(f"  {person['name']} (age {person['age']})")
    
    # Range query on salary
    print("\nPeople with salary 80k-95k:")
    high_earners = db_index.range_query("salary", 80000, 95000)
    for person in high_earners:
        print(f"  {person['name']} (salary ${person['salary']:,})")
    
    # Field statistics
    print("\nField Statistics:")
    for field in ["age", "salary", "city"]:
        stats = db_index.get_field_statistics(field)
        print(f"{field}: {stats}")
    
    # Export and import demonstration
    print("\nExport/Import Demonstration:")
    db_index.export_to_json("temp_database.json")
    print("Database exported to temp_database.json")
    
    # Create new database and import
    new_db = DatabaseIndex()
    new_db.import_from_json("temp_database.json")
    print(f"Imported database stats: {new_db.get_index_stats()}")
    
    # Verify data integrity
    original_records = db_index.get_all_records()
    imported_records = new_db.get_all_records()
    print(f"Data integrity check: {len(original_records) == len(imported_records)}")

if __name__ == "__main__":
    # Run the main demo
    run_avl_tree_demo()
    
    # Run additional demonstrations
    demonstrate_rotation_scenarios()
    benchmark_comparison()
    demonstrate_database_features() 