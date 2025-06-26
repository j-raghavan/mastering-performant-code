"""
Chapter 10: Trie & Compressed Trie

This module contains implementations of trie data structures for efficient
string storage and retrieval, including standard tries, compressed tries,
and Unicode-aware variants.
"""

from src.chapter_10.trie import Trie, TrieNode
from src.chapter_10.compressed_trie import CompressedTrie, CompressedTrieNode
from src.chapter_10.unicode_trie import UnicodeTrie
from src.chapter_10.autocomplete import AutocompleteSystem
from src.chapter_10.spell_checker import SpellChecker
from src.chapter_10.analyzer import TrieAnalyzer, TrieStats
from src.chapter_10.demo import benchmark_trie_performance, demonstrate_real_world_applications

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