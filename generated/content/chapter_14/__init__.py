"""
Chapter 14: Bloom Filter & Probabilistic Counting

This module provides implementations of various Bloom filter variants:
- Basic Bloom Filter
- Counting Bloom Filter  
- Scalable Bloom Filter
- Performance analysis tools
- Real-world applications
"""

from .bloom_filter import BloomFilter
from .counting_bloom_filter import CountingBloomFilter
from .scalable_bloom_filter import ScalableBloomFilter
from .analyzer import BloomFilterAnalyzer, BloomFilterStats
from .applications import SpellChecker, WebCache
from .demo import (
    demonstrate_bloom_filters,
    demonstrate_counting_bloom_filter,
    demonstrate_scalable_bloom_filter,
    demonstrate_spell_checker,
    demonstrate_web_cache
)

__all__ = [
    'BloomFilter',
    'CountingBloomFilter', 
    'ScalableBloomFilter',
    'BloomFilterAnalyzer',
    'BloomFilterStats',
    'SpellChecker',
    'WebCache',
    'demonstrate_bloom_filters',
    'demonstrate_counting_bloom_filter',
    'demonstrate_scalable_bloom_filter',
    'demonstrate_spell_checker',
    'demonstrate_web_cache'
] 