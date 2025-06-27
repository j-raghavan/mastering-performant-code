"""
Chapter 10: Trie & Compressed Trie

This module contains implementations of trie data structures for efficient
string storage and retrieval, including standard tries, compressed tries,
and Unicode-aware variants.
"""

from .trie import Trie, TrieNode
from .compressed_trie import CompressedTrie, CompressedTrieNode
from .unicode_trie import UnicodeTrie
from .autocomplete import AutocompleteSystem
from .spell_checker import SpellChecker
from .analyzer import TrieAnalyzer, TrieStats
from .demo import benchmark_trie_performance, demonstrate_real_world_applications

__all__ = [
    'Trie',
    'TrieNode',
    'CompressedTrie',
    'CompressedTrieNode',
    'UnicodeTrie',
    'AutocompleteSystem',
    'SpellChecker',
    'TrieAnalyzer',
    'TrieStats',
    'benchmark_trie_performance',
    'demonstrate_real_world_applications'
] 