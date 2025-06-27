"""
Bloom Filter Demonstrations

This module provides comprehensive demonstrations of all Bloom filter
implementations and real-world applications.
"""

import timeit
from typing import List, Dict, Any
from .bloom_filter import BloomFilter
from .counting_bloom_filter import CountingBloomFilter
from .scalable_bloom_filter import ScalableBloomFilter
from .analyzer import BloomFilterAnalyzer
from .applications import SpellChecker, WebCache, DuplicateDetector, EmailFilter, URLShortener

def demonstrate_bloom_filters():
    """Demonstrate Bloom filter implementations with performance analysis."""
    print("=== Bloom Filter Demonstration ===\n")
    
    # Test parameters
    test_sizes = [1000, 10000, 100000]
    false_positive_rates = [0.01, 0.05, 0.1]
    
    for size in test_sizes:
        print(f"Testing with {size} elements:")
        print("-" * 50)
        
        for fpr in false_positive_rates:
            print(f"\nFalse positive rate: {fpr}")
            
            # Create test data
            test_items = [f"item_{i}" for i in range(size)]
            non_member_items = [f"non_member_{i}" for i in range(size)]
            
            # Test basic Bloom filter
            bf = BloomFilter(expected_elements=size, false_positive_rate=fpr)
            
            # Performance analysis
            analyzer = BloomFilterAnalyzer()
            stats = analyzer.analyze_bloom_filter(bf)
            benchmark_results = analyzer.benchmark_operations(bf, test_items, non_member_items)
            false_positive_results = analyzer.measure_false_positives(bf, test_items, non_member_items)
            comparison_results = analyzer.compare_with_set(bf, test_items, test_items + non_member_items)
            
            print(f"  Memory usage: {stats.memory_usage} bytes")
            print(f"  Add time: {benchmark_results['add_time']:.6f} seconds per item")
            print(f"  Query time: {benchmark_results['contains_member_time']:.6f} seconds per item")
            print(f"  Actual FPR: {false_positive_results['actual_false_positive_rate']:.4f}")
            print(f"  Memory ratio vs set: {comparison_results['memory_ratio']:.2f}x")
            print(f"  Query speedup vs set: {comparison_results['speedup_query']:.2f}x")
    
    print("\n" + "="*60 + "\n")

def demonstrate_counting_bloom_filter():
    """Demonstrate counting Bloom filter with deletion support."""
    print("=== Counting Bloom Filter Demonstration ===\n")
    
    # Create counting Bloom filter
    cbf = CountingBloomFilter(expected_elements=1000, false_positive_rate=0.01)
    
    # Add items
    items = ["apple", "banana", "cherry", "date", "elderberry"]
    for item in items:
        cbf.add(item)
    
    print(f"Added {len(items)} items")
    print(f"Contains 'apple': {cbf.contains('apple')}")
    print(f"Contains 'grape': {cbf.contains('grape')}")
    
    # Remove item
    removed = cbf.remove("banana")
    print(f"Removed 'banana': {removed}")
    print(f"Contains 'banana' after removal: {cbf.contains('banana')}")
    
    # Show counter distribution
    distribution = cbf.get_counter_distribution()
    print(f"Counter distribution: {distribution}")
    
    # Show utilization stats
    stats = cbf.get_utilization_stats()
    print(f"Utilization stats: {stats}")
    
    print("\n" + "="*60 + "\n")

def demonstrate_scalable_bloom_filter():
    """Demonstrate scalable Bloom filter with dynamic growth."""
    print("=== Scalable Bloom Filter Demonstration ===\n")
    
    # Create scalable Bloom filter
    sbf = ScalableBloomFilter(initial_capacity=100, false_positive_rate=0.01)
    
    # Add items gradually
    for i in range(500):
        sbf.add(f"item_{i}")
        
        if i % 100 == 0:
            stats = sbf.get_filter_stats()
            print(f"After {i} items: {len(stats)} filters, "
                  f"FPR: {sbf.get_false_positive_rate():.4f}")
    
    print(f"Final state: {len(sbf.filters)} filters")
    print(f"Total elements: {sbf.get_total_elements()}")
    print(f"Overall FPR: {sbf.get_false_positive_rate():.4f}")
    print(f"Memory usage: {sbf.get_memory_usage()} bytes")
    
    # Show efficiency metrics
    efficiency = sbf.get_efficiency_metrics()
    print(f"Efficiency metrics: {efficiency}")
    
    print("\n" + "="*60 + "\n")

def demonstrate_spell_checker():
    """Demonstrate spell checker application."""
    print("=== Spell Checker Application ===\n")
    
    # Sample dictionary
    dictionary = [
        "hello", "world", "python", "programming", "computer", "science",
        "algorithm", "data", "structure", "bloom", "filter", "efficient",
        "memory", "performance", "optimization", "analysis", "testing"
    ]
    
    # Create spell checker
    spell_checker = SpellChecker(dictionary, false_positive_rate=0.01)
    
    # Test some words
    test_words = ["hello", "world", "pythn", "programming", "algoritm", "xyz"]
    
    print("Spell checking results:")
    for word in test_words:
        is_correct = spell_checker.is_correctly_spelled(word)
        print(f"  '{word}': {'✓' if is_correct else '✗'}")
    
    # Check a sentence
    text = "hello world pythn programming algoritm"
    results = spell_checker.check_text(text)
    
    print(f"\nText analysis: '{text}'")
    for word, pos, is_correct in results:
        status = "✓" if is_correct else "✗"
        print(f"  '{word}' (pos {pos}): {status}")
    
    # Show statistics
    stats = spell_checker.get_stats()
    print(f"\nDictionary size: {stats['dictionary_size']}")
    print(f"Memory efficiency: {stats['memory_efficiency']:.2f}x")
    
    print("\n" + "="*60 + "\n")

def demonstrate_web_cache():
    """Demonstrate web cache application."""
    print("=== Web Cache Application ===\n")
    
    # Create web cache
    cache = WebCache(expected_urls=1000, false_positive_rate=0.01)
    
    # Simulate adding URLs to cache
    cached_urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3"
    ]
    
    for url in cached_urls:
        cache.add_url(url)
    
    # Simulate cache access
    test_urls = [
        ("https://example.com/page1", True),   # Actually cached
        ("https://example.com/page2", True),   # Actually cached
        ("https://example.com/page4", False),  # Not cached
        ("https://example.com/page5", False),  # Not cached
        ("https://example.com/page6", False)   # Not cached
    ]
    
    print("Cache access simulation:")
    for url, actually_cached in test_urls:
        result = cache.simulate_cache_access(url, actually_cached)
        status = "cached" if actually_cached else "not cached"
        print(f"  {url} ({status}): {result}")
    
    # Show cache statistics
    stats = cache.get_cache_stats()
    print(f"\nCache statistics:")
    print(f"  Hit rate: {stats['hit_rate']:.2%}")
    print(f"  Miss rate: {stats['miss_rate']:.2%}")
    print(f"  False positive rate: {stats['false_positive_rate']:.2%}")
    print(f"  Total requests: {stats['total_requests']}")
    
    print("\n" + "="*60 + "\n")

def demonstrate_duplicate_detector():
    """Demonstrate duplicate detector application."""
    print("=== Duplicate Detector Application ===\n")
    
    # Create duplicate detector
    detector = DuplicateDetector(expected_items=1000, false_positive_rate=0.01)
    
    # Simulate processing items
    items = ["item1", "item2", "item1", "item3", "item2", "item4", "item5"]
    
    print("Processing items:")
    for item in items:
        is_duplicate = detector.process_item(item)
        status = "DUPLICATE" if is_duplicate else "NEW"
        print(f"  {item}: {status}")
    
    # Show statistics
    stats = detector.get_stats()
    print(f"\nDuplicate detection statistics:")
    print(f"  Total items: {stats['total_items']}")
    print(f"  Unique items: {stats['unique_items']}")
    print(f"  Duplicates found: {stats['duplicates_found']}")
    print(f"  Duplicate rate: {stats['duplicate_rate']:.2%}")
    
    print("\n" + "="*60 + "\n")

def demonstrate_email_filter():
    """Demonstrate email filter application."""
    print("=== Email Filter Application ===\n")
    
    # Create email filter with spam patterns
    spam_patterns = ["free", "money", "winner", "lottery", "viagra", "click", "urgent"]
    email_filter = EmailFilter(spam_patterns, false_positive_rate=0.01)
    
    # Simulate emails
    emails = [
        ("Hello, you have won a free lottery prize!", True),  # Spam
        ("Meeting tomorrow at 3 PM", False),                  # Ham
        ("Click here to get free money now!", True),          # Spam
        ("Project update for Q4", False),                     # Ham
        ("Urgent: You are a winner!", True),                  # Spam
    ]
    
    print("Email filtering results:")
    for email_content, is_actually_spam in emails:
        detected_as_spam = email_filter.is_spam(email_content)
        actual_status = "SPAM" if is_actually_spam else "HAM"
        detected_status = "SPAM" if detected_as_spam else "HAM"
        print(f"  '{email_content[:30]}...' ({actual_status}): {detected_status}")
    
    # Show processing results
    results = email_filter.simulate_email_processing(emails)
    print(f"\nProcessing results:")
    print(f"  Correct spam detections: {results['correct_spam_detections']}")
    print(f"  False spam detections: {results['false_spam_detections']}")
    print(f"  Missed spam: {results['missed_spam']}")
    print(f"  Correct ham detections: {results['correct_ham_detections']}")
    
    print("\n" + "="*60 + "\n")

def demonstrate_url_shortener():
    """Demonstrate URL shortener application."""
    print("=== URL Shortener Application ===\n")
    
    # Create URL shortener
    shortener = URLShortener(expected_urls=1000, false_positive_rate=0.01)
    
    # Simulate URL shortening
    urls = [
        "https://example.com/very/long/url/1",
        "https://example.com/very/long/url/2",
        "https://example.com/very/long/url/1",  # Duplicate
        "https://example.com/very/long/url/3",
        "https://example.com/very/long/url/2",  # Duplicate
    ]
    
    print("URL shortening results:")
    for url in urls:
        short_url = shortener.shorten_url(url)
        print(f"  {url[:30]}... -> {short_url}")
    
    # Show statistics
    stats = shortener.get_stats()
    print(f"\nURL shortener statistics:")
    print(f"  URLs processed: {stats['urls_processed']}")
    print(f"  Unique URLs: {stats['unique_urls']}")
    print(f"  Duplicates found: {stats['duplicates_found']}")
    print(f"  Duplicate rate: {stats['duplicate_rate']:.2%}")
    
    print("\n" + "="*60 + "\n")

def benchmark_bloom_filter_variants():
    """Compare different Bloom filter implementations."""
    print("=== Bloom Filter Variants Benchmark ===\n")
    
    # Test parameters
    sizes = [1000, 10000, 100000]
    false_positive_rates = [0.01, 0.05]
    
    for size in sizes:
        print(f"Testing with {size} elements:")
        print("-" * 50)
        
        for fpr in false_positive_rates:
            print(f"\nFalse positive rate: {fpr}")
            
            # Test data
            test_items = [f"item_{i}" for i in range(size)]
            query_items = test_items + [f"query_{i}" for i in range(size)]
            
            # Basic Bloom filter
            bf = BloomFilter(expected_elements=size, false_positive_rate=fpr)
            
            bf_add_time = timeit.timeit(
                lambda: [bf.add(item) for item in test_items],
                number=1
            )
            
            bf_query_time = timeit.timeit(
                lambda: [bf.contains(item) for item in query_items],
                number=10
            )
            
            # Counting Bloom filter
            cbf = CountingBloomFilter(expected_elements=size, false_positive_rate=fpr)
            
            cbf_add_time = timeit.timeit(
                lambda: [cbf.add(item) for item in test_items],
                number=1
            )
            
            cbf_query_time = timeit.timeit(
                lambda: [cbf.contains(item) for item in query_items],
                number=10
            )
            
            # Scalable Bloom filter
            sbf = ScalableBloomFilter(initial_capacity=size//10, false_positive_rate=fpr)
            
            sbf_add_time = timeit.timeit(
                lambda: [sbf.add(item) for item in test_items],
                number=1
            )
            
            sbf_query_time = timeit.timeit(
                lambda: [sbf.contains(item) for item in query_items],
                number=10
            )
            
            print(f"  Basic BF - Add: {bf_add_time:.4f}s, Query: {bf_query_time:.4f}s, "
                  f"Memory: {bf.get_memory_usage()} bytes")
            print(f"  Counting BF - Add: {cbf_add_time:.4f}s, Query: {cbf_query_time:.4f}s, "
                  f"Memory: {cbf.get_memory_usage()} bytes")
            print(f"  Scalable BF - Add: {sbf_add_time:.4f}s, Query: {sbf_query_time:.4f}s, "
                  f"Memory: {sbf.get_memory_usage()} bytes")
    
    print("\n" + "="*60 + "\n")

def benchmark_false_positive_rates():
    """Benchmark false positive rates across different configurations."""
    print("=== False Positive Rate Analysis ===\n")
    
    # Test configurations
    configs = [
        (1000, 0.01), (1000, 0.05), (1000, 0.1),
        (10000, 0.01), (10000, 0.05), (10000, 0.1),
        (100000, 0.01), (100000, 0.05), (100000, 0.1)
    ]
    
    print("Size\tTarget FPR\tActual FPR\tMemory\tHash Count")
    print("-" * 60)
    
    for size, target_fpr in configs:
        # Create Bloom filter
        bf = BloomFilter(expected_elements=size, false_positive_rate=target_fpr)
        
        # Add elements
        test_items = [f"item_{i}" for i in range(size)]
        for item in test_items:
            bf.add(item)
        
        # Test false positives
        non_member_items = [f"non_member_{i}" for i in range(size)]
        false_positives = sum(1 for item in non_member_items if bf.contains(item))
        actual_fpr = false_positives / len(non_member_items)
        
        print(f"{size}\t{target_fpr:.3f}\t\t{actual_fpr:.3f}\t\t"
              f"{bf.get_memory_usage()}\t{bf.hash_count}")
    
    print("\n" + "="*60 + "\n")

def benchmark_memory_efficiency():
    """Benchmark memory efficiency vs Python set."""
    print("=== Memory Efficiency Comparison ===\n")
    
    sizes = [1000, 10000, 100000]
    
    print("Size\tBloom Filter\tPython Set\tRatio\tFPR")
    print("-" * 50)
    
    for size in sizes:
        # Bloom filter
        bf = BloomFilter(expected_elements=size, false_positive_rate=0.01)
        test_items = [f"item_{i}" for i in range(size)]
        
        for item in test_items:
            bf.add(item)
        
        bloom_memory = bf.get_memory_usage()
        
        # Python set
        test_set = set(test_items)
        set_memory = sys.getsizeof(test_set) + sum(sys.getsizeof(item) for item in test_set)
        
        ratio = bloom_memory / set_memory
        fpr = bf.get_false_positive_rate()
        
        print(f"{size}\t{bloom_memory}\t\t{set_memory}\t\t{ratio:.2f}x\t{fpr:.4f}")
    
    print("\n" + "="*60 + "\n")

def generate_comprehensive_report():
    """Generate a comprehensive performance report."""
    print("=== Comprehensive Performance Report ===\n")
    
    # Test with a medium-sized dataset
    size = 10000
    test_items = [f"item_{i}" for i in range(size)]
    non_member_items = [f"non_member_{i}" for i in range(size)]
    
    # Test basic Bloom filter
    bf = BloomFilter(expected_elements=size, false_positive_rate=0.01)
    
    # Generate report
    report = BloomFilterAnalyzer.generate_performance_report(bf, test_items, non_member_items)
    print(report)
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    # Run all demonstrations
    demonstrate_bloom_filters()
    demonstrate_counting_bloom_filter()
    demonstrate_scalable_bloom_filter()
    demonstrate_spell_checker()
    demonstrate_web_cache()
    demonstrate_duplicate_detector()
    demonstrate_email_filter()
    demonstrate_url_shortener()
    
    # Run benchmarks
    benchmark_bloom_filter_variants()
    benchmark_false_positive_rates()
    benchmark_memory_efficiency()
    
    # Generate comprehensive report
    generate_comprehensive_report() 