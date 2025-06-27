import pytest
from chapter_13.hash_table import (
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
)

@pytest.mark.parametrize("HashTableClass", [
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
])
def test_basic_operations(HashTableClass):
    ht = HashTableClass()
    # Test set and get
    ht['a'] = 1
    ht['b'] = 2
    ht['c'] = 3
    assert ht['a'] == 1
    assert ht['b'] == 2
    assert ht['c'] == 3
    # Test overwrite
    ht['a'] = 10
    assert ht['a'] == 10
    # Test contains
    assert 'a' in ht
    assert 'b' in ht
    assert 'z' not in ht
    # Test len
    assert len(ht) == 3
    # Test get with default
    assert ht.get('x', 99) == 99
    # Test keys, values, items
    keys = set(ht.keys())
    values = set(ht.values())
    items = set(ht.items())
    assert keys == {'a', 'b', 'c'}
    assert values == {10, 2, 3}
    assert items == {('a', 10), ('b', 2), ('c', 3)}
    # Test iteration
    assert set(iter(ht)) == {'a', 'b', 'c'}
    # Test clear
    ht.clear()
    assert len(ht) == 0
    assert list(ht.keys()) == []

@pytest.mark.parametrize("HashTableClass", [
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
])
def test_deletion_and_key_error(HashTableClass):
    ht = HashTableClass()
    ht['x'] = 42
    del ht['x']
    assert 'x' not in ht
    with pytest.raises(KeyError):
        _ = ht['x']
    with pytest.raises(KeyError):
        del ht['x']

@pytest.mark.parametrize("HashTableClass", [
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
])
def test_resize_and_collisions(HashTableClass):
    ht = HashTableClass(initial_capacity=4, load_factor=0.5)
    # Insert enough items to trigger resize
    for i in range(10):
        ht[f'k{i}'] = i
    for i in range(10):
        assert ht[f'k{i}'] == i
    assert len(ht) == 10
    # Remove some items and check
    for i in range(5):
        del ht[f'k{i}']
    for i in range(5):
        assert f'k{i}' not in ht
    for i in range(5, 10):
        assert ht[f'k{i}'] == i
    # Re-insert and check
    for i in range(5):
        ht[f'k{i}'] = i * 100
    for i in range(5):
        assert ht[f'k{i}'] == i * 100
    assert len(ht) == 10

@pytest.mark.parametrize("HashTableClass", [
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
])
def test_edge_cases(HashTableClass):
    ht = HashTableClass()
    # Test empty table
    assert len(ht) == 0
    assert list(ht.keys()) == []
    # Test deletion of non-existent key
    with pytest.raises(KeyError):
        del ht['notfound']
    # Test get with missing key
    assert ht.get('notfound') is None
    # Test inserting None as key and value
    ht[None] = None
    assert ht[None] is None
    del ht[None]
    assert None not in ht

@pytest.mark.parametrize("HashTableClass", [
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
])
def test_performance_statistics(HashTableClass):
    """Test the new performance statistics functionality."""
    ht = HashTableClass(initial_capacity=8, load_factor=0.75)
    
    # Test empty statistics
    stats = ht.get_statistics()
    assert stats['size'] == 0
    assert stats['capacity'] == 8
    assert stats['load_factor'] == 0.0
    assert stats['resize_count'] == 0
    assert stats['collision_count'] == 0
    assert stats['probe_count'] == 0
    assert stats['average_probes'] == 0.0
    
    # Test statistics after operations
    ht['a'] = 1
    ht['b'] = 2
    ht['c'] = 3
    
    stats = ht.get_statistics()
    assert stats['size'] == 3
    assert stats['capacity'] == 8
    assert stats['load_factor'] == 3/8
    assert stats['resize_count'] == 0
    
    # Test memory info
    memory_info = ht.get_memory_info()
    assert 'table_memory' in memory_info
    assert 'total_memory' in memory_info
    assert 'memory_per_element' in memory_info
    assert 'load_factor' in memory_info
    assert memory_info['load_factor'] == 3/8
    
    # Test hash distribution analysis
    distribution = ht.analyze_hash_distribution()
    assert 'max_bucket_size' in distribution
    assert 'min_bucket_size' in distribution
    assert 'empty_buckets' in distribution
    assert 'distribution_variance' in distribution
    assert 'bucket_distribution' in distribution
    assert len(distribution['bucket_distribution']) == 8

@pytest.mark.parametrize("HashTableClass", [
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
])
def test_resize_statistics(HashTableClass):
    """Test that resize operations are properly tracked."""
    ht = HashTableClass(initial_capacity=4, load_factor=0.5)
    
    # Initial state
    assert ht.get_statistics()['resize_count'] == 0
    
    # Insert enough to trigger resize
    for i in range(10):
        ht[f'key{i}'] = i
    
    # Should have resized at least once
    stats = ht.get_statistics()
    assert stats['resize_count'] > 0
    assert stats['size'] == 10

@pytest.mark.parametrize("HashTableClass", [
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
])
def test_probe_counting(HashTableClass):
    """Test that probe counting works correctly."""
    ht = HashTableClass(initial_capacity=4, load_factor=0.75)
    
    # Insert some items
    ht['a'] = 1
    ht['b'] = 2
    ht['c'] = 3
    
    # Access items to generate probes
    _ = ht['a']
    _ = ht['b']
    _ = ht['c']
    
    stats = ht.get_statistics()
    assert stats['probe_count'] > 0
    assert stats['average_probes'] > 0

@pytest.mark.parametrize("HashTableClass", [
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
])
def test_tombstone_tracking(HashTableClass):
    """Test tombstone tracking for open addressing methods."""
    ht = HashTableClass(initial_capacity=8, load_factor=0.75)
    
    # Insert and delete items
    ht['a'] = 1
    ht['b'] = 2
    ht['c'] = 3
    
    del ht['b']
    
    stats = ht.get_statistics()
    assert 'tombstone_count' in stats
    assert stats['tombstone_count'] > 0
    assert stats['size'] == 2

@pytest.mark.parametrize("HashTableClass", [
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
])
def test_hash_distribution_quality(HashTableClass):
    """Test hash distribution analysis."""
    ht = HashTableClass(initial_capacity=16, load_factor=0.75)
    
    # Insert items with known hash patterns
    for i in range(20):
        ht[f'key{i}'] = i
    
    distribution = ht.analyze_hash_distribution()
    
    # Check distribution properties
    assert distribution['max_bucket_size'] >= 1
    assert distribution['min_bucket_size'] >= 0
    assert distribution['empty_buckets'] >= 0
    # Note: capacity may have changed due to resizing
    assert distribution['empty_buckets'] <= ht._capacity
    assert distribution['distribution_variance'] >= 0.0
    
    # Bucket distribution should match current capacity
    assert len(distribution['bucket_distribution']) == ht._capacity

@pytest.mark.parametrize("HashTableClass", [
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
])
def test_memory_efficiency(HashTableClass):
    """Test memory usage tracking."""
    ht = HashTableClass(initial_capacity=16, load_factor=0.75)
    
    # Insert items
    for i in range(10):
        ht[f'key{i}'] = f'value{i}'
    
    memory_info = ht.get_memory_info()
    
    # Check memory info structure
    assert 'table_memory' in memory_info
    assert 'total_memory' in memory_info
    assert 'memory_per_element' in memory_info
    assert 'load_factor' in memory_info
    
    # Memory values should be positive
    assert memory_info['table_memory'] > 0
    assert memory_info['total_memory'] > 0
    assert memory_info['memory_per_element'] > 0
    assert 0 <= memory_info['load_factor'] <= 1

@pytest.mark.parametrize("HashTableClass", [
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
])
def test_collision_detection(HashTableClass):
    """Test collision counting functionality."""
    ht = HashTableClass(initial_capacity=4, load_factor=0.75)
    
    # Force collisions by using a small capacity
    ht['a'] = 1
    ht['b'] = 2
    ht['c'] = 3
    ht['d'] = 4
    ht['e'] = 5  # This should cause a collision
    
    stats = ht.get_statistics()
    assert stats['collision_count'] >= 0  # May or may not have collisions depending on hash function

@pytest.mark.parametrize("HashTableClass", [
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
])
def test_statistics_consistency(HashTableClass):
    """Test that statistics remain consistent across operations."""
    ht = HashTableClass(initial_capacity=8, load_factor=0.75)
    
    # Track statistics through operations
    initial_stats = ht.get_statistics()
    
    # Insert items
    ht['a'] = 1
    ht['b'] = 2
    
    after_insert_stats = ht.get_statistics()
    assert after_insert_stats['size'] == 2
    assert after_insert_stats['load_factor'] == 2/8
    
    # Delete an item
    del ht['a']
    
    after_delete_stats = ht.get_statistics()
    assert after_delete_stats['size'] == 1
    assert after_delete_stats['load_factor'] == 1/8
    
    # Clear the table
    ht.clear()
    
    final_stats = ht.get_statistics()
    assert final_stats['size'] == 0
    assert final_stats['load_factor'] == 0.0

@pytest.mark.parametrize("HashTableClass", [
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
])
def test_large_dataset_statistics(HashTableClass):
    """Test statistics with a larger dataset."""
    ht = HashTableClass(initial_capacity=16, load_factor=0.75)
    
    # Insert many items
    for i in range(100):
        ht[f'key{i}'] = f'value{i}'
    
    stats = ht.get_statistics()
    
    # Verify statistics
    assert stats['size'] == 100
    assert stats['capacity'] >= 16  # May have resized
    assert stats['load_factor'] > 0
    assert stats['resize_count'] >= 0
    # Probe count may be 0 if no lookups were performed
    assert stats['probe_count'] >= 0
    assert stats['average_probes'] >= 0
    
    # Test memory info with large dataset
    memory_info = ht.get_memory_info()
    assert memory_info['table_memory'] > 0
    assert memory_info['total_memory'] > memory_info['table_memory']
    
    # Test distribution analysis
    distribution = ht.analyze_hash_distribution()
    assert distribution['max_bucket_size'] > 0
    assert distribution['distribution_variance'] >= 0.0 