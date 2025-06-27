"""
Real-world applications demonstrating hash table usage.

This module provides practical examples of how hash tables are used
in real-world scenarios like caching, symbol tables, and database indexing.
"""

from typing import TypeVar, Generic, Optional, Any, Dict, List, Tuple
from collections import OrderedDict
import time
from .hash_table import (
    HashTableInterface,
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
)

K = TypeVar('K')
V = TypeVar('V')


class LRUCache(Generic[K, V]):
    """
    Least Recently Used (LRU) Cache implementation using hash table.
    
    This is a common caching strategy where the least recently used item
    is evicted when the cache reaches its capacity limit.
    
    Real-world applications:
    - Web browser cache
    - Database query result caching
    - CPU cache management
    - Memory management systems
    """
    
    def __init__(self, capacity: int, hash_table_class: type = SeparateChainingHashTable):
        self._capacity = capacity
        self._cache: HashTableInterface[K, Tuple[V, float]] = hash_table_class()
        self._access_times: Dict[K, float] = {}
    
    def get(self, key: K) -> Optional[V]:
        """Get value from cache, updating access time."""
        if key in self._cache:
            value, _ = self._cache[key]
            self._access_times[key] = time.time()
            return value
        return None
    
    def put(self, key: K, value: V) -> None:
        """Put value in cache, evicting LRU item if necessary."""
        current_time = time.time()
        
        if key in self._cache:
            # Update existing item
            self._cache[key] = (value, current_time)
            self._access_times[key] = current_time
        else:
            # Check if we need to evict
            if len(self._cache) >= self._capacity:
                self._evict_lru()
            
            # Add new item
            self._cache[key] = (value, current_time)
            self._access_times[key] = current_time
    
    def _evict_lru(self) -> None:
        """Evict the least recently used item."""
        if not self._access_times:
            return
        
        lru_key = min(self._access_times, key=self._access_times.get)
        del self._cache[lru_key]
        del self._access_times[lru_key]
    
    def __len__(self) -> int:
        return len(self._cache)
    
    def __contains__(self, key: K) -> bool:
        return key in self._cache
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get cache statistics."""
        cache_stats = self._cache.get_statistics()
        return {
            'capacity': self._capacity,
            'size': len(self._cache),
            'utilization': len(self._cache) / self._capacity,
            'cache_stats': cache_stats
        }


class SymbolTable:
    """
    Compiler symbol table implementation using hash table.
    
    Symbol tables are used in compilers to track variables, functions,
    and other symbols during compilation. They need fast lookup and
    scope management.
    
    Real-world applications:
    - Programming language compilers
    - Interpreters
    - Code analysis tools
    - IDE features (autocomplete, refactoring)
    """
    
    def __init__(self, hash_table_class: type = DoubleHashingHashTable):
        self._scopes: List[HashTableInterface[str, Dict[str, Any]]] = [hash_table_class()]
        self._current_scope = 0
    
    def enter_scope(self) -> None:
        """Enter a new scope."""
        self._scopes.append(type(self._scopes[0])())
        self._current_scope += 1
    
    def exit_scope(self) -> None:
        """Exit the current scope."""
        if self._current_scope > 0:
            self._scopes.pop()
            self._current_scope -= 1
    
    def insert(self, name: str, symbol_type: str, **attributes) -> None:
        """Insert a symbol into the current scope."""
        symbol_info = {
            'type': symbol_type,
            'scope': self._current_scope,
            'line_number': attributes.get('line_number', 0),
            **attributes
        }
        self._scopes[self._current_scope][name] = symbol_info
    
    def lookup(self, name: str) -> Optional[Dict[str, Any]]:
        """Look up a symbol, searching from current scope outward."""
        for i in range(self._current_scope, -1, -1):
            if name in self._scopes[i]:
                return self._scopes[i][name]
        return None
    
    def lookup_current_scope(self, name: str) -> Optional[Dict[str, Any]]:
        """Look up a symbol only in the current scope."""
        if name in self._scopes[self._current_scope]:
            return self._scopes[self._current_scope][name]
        return None
    
    def get_all_symbols(self) -> Dict[str, Dict[str, Any]]:
        """Get all symbols from all scopes."""
        all_symbols = {}
        for i, scope in enumerate(self._scopes):
            for name, info in scope.items():
                all_symbols[name] = info
        return all_symbols
    
    def get_scope_depth(self) -> int:
        """Get current scope depth."""
        return self._current_scope


class DatabaseIndex:
    """
    Simple database index implementation using hash table.
    
    Database indexes are used to speed up queries by providing
    fast access to data based on key values.
    
    Real-world applications:
    - Database management systems
    - Search engines
    - File systems
    - Key-value stores
    """
    
    def __init__(self, hash_table_class: type = LinearProbingHashTable):
        self._index: HashTableInterface[Any, List[int]] = hash_table_class()
        self._data: List[Dict[str, Any]] = []
        self._next_id = 0
    
    def insert_record(self, **fields) -> int:
        """Insert a record and update all indexes."""
        record_id = self._next_id
        self._next_id += 1
        
        # Add record to data
        record = {'id': record_id, **fields}
        self._data.append(record)
        
        # Update indexes for each field
        for field_name, value in fields.items():
            if value not in self._index:
                self._index[value] = []
            self._index[value].append(record_id)
        
        return record_id
    
    def find_by_field(self, field_name: str, value: Any) -> List[Dict[str, Any]]:
        """Find records by field value using index."""
        if value not in self._index:
            return []
        
        record_ids = self._index[value]
        return [self._data[record_id] for record_id in record_ids 
                if record_id < len(self._data)]
    
    def delete_record(self, record_id: int) -> bool:
        """Delete a record and update indexes."""
        if record_id >= len(self._data) or self._data[record_id] is None:
            return False
        
        record = self._data[record_id]
        
        # Remove from indexes
        for field_name, value in record.items():
            if field_name == 'id':
                continue
            if value in self._index:
                if record_id in self._index[value]:
                    self._index[value].remove(record_id)
                if not self._index[value]:
                    del self._index[value]
        
        # Mark as deleted
        self._data[record_id] = None
        return True
    
    def get_all_records(self) -> List[Dict[str, Any]]:
        """Get all non-deleted records."""
        return [record for record in self._data if record is not None]
    
    def get_index_statistics(self) -> Dict[str, Any]:
        """Get index performance statistics."""
        index_stats = self._index.get_statistics()
        return {
            'total_records': len(self.get_all_records()),
            'index_size': len(self._index),
            'index_stats': index_stats,
            'memory_info': self._index.get_memory_info()
        }


class WordFrequencyCounter:
    """
    Word frequency counter using hash table for efficient counting.
    
    This is a common text analysis application that counts the
    frequency of words in a text corpus.
    
    Real-world applications:
    - Text analysis and NLP
    - Search engine ranking
    - Plagiarism detection
    - Language modeling
    """
    
    def __init__(self, hash_table_class: type = SeparateChainingHashTable):
        self._frequencies: HashTableInterface[str, int] = hash_table_class()
        self._total_words = 0
    
    def add_text(self, text: str) -> None:
        """Add text and count word frequencies."""
        import re
        
        # Simple word tokenization
        words = re.findall(r'\b\w+\b', text.lower())
        
        for word in words:
            self._frequencies[word] = self._frequencies.get(word, 0) + 1
            self._total_words += 1
    
    def get_frequency(self, word: str) -> int:
        """Get frequency of a specific word."""
        return self._frequencies.get(word.lower(), 0)
    
    def get_most_common(self, n: int = 10) -> List[Tuple[str, int]]:
        """Get the n most common words."""
        items = [(word, freq) for word, freq in self._frequencies.items()]
        items.sort(key=lambda x: x[1], reverse=True)
        return items[:n]
    
    def get_word_probability(self, word: str) -> float:
        """Get probability of a word occurring."""
        if self._total_words == 0:
            return 0.0
        return self.get_frequency(word) / self._total_words
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get text analysis statistics."""
        freq_stats = self._frequencies.get_statistics()
        return {
            'total_words': self._total_words,
            'unique_words': len(self._frequencies),
            'average_frequency': self._total_words / len(self._frequencies) if self._frequencies else 0,
            'frequency_stats': freq_stats
        }
    
    def get_total_words(self) -> int:
        """Get the total number of words processed."""
        return self._total_words


class SpellChecker:
    """
    Simple spell checker using hash table for dictionary lookup.
    
    Spell checkers use hash tables to quickly check if words
    are in a dictionary of valid words.
    
    Real-world applications:
    - Text editors and word processors
    - Search engines
    - Auto-correct systems
    - Natural language processing
    """
    
    def __init__(self, dictionary_words: List[str], hash_table_class: type = QuadraticProbingHashTable):
        self._dictionary: HashTableInterface[str, bool] = hash_table_class()
        
        # Build dictionary
        for word in dictionary_words:
            self._dictionary[word.lower()] = True
    
    def is_correct(self, word: str) -> bool:
        """Check if a word is spelled correctly."""
        return word.lower() in self._dictionary
    
    def get_suggestions(self, word: str, max_suggestions: int = 5) -> List[str]:
        """Get spelling suggestions for a word."""
        if self.is_correct(word):
            return []
        
        suggestions = []
        word_lower = word.lower()
        
        # Simple edit distance-based suggestions
        for dict_word in self._dictionary.keys():
            if self._edit_distance(word_lower, dict_word) <= 2:
                suggestions.append(dict_word)
                if len(suggestions) >= max_suggestions:
                    break
        
        return suggestions
    
    def _edit_distance(self, word1: str, word2: str) -> int:
        """Calculate Levenshtein edit distance between two words."""
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i-1] == word2[j-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
        
        return dp[m][n]
    
    def get_dictionary_size(self) -> int:
        """Get the size of the dictionary."""
        return len(self._dictionary)


def demonstrate_applications():
    """Demonstrate all the real-world applications."""
    print("="*80)
    print("REAL-WORLD HASH TABLE APPLICATIONS")
    print("="*80)
    
    # 1. LRU Cache Demo
    print("\n1. LRU CACHE DEMONSTRATION")
    print("-" * 40)
    cache = LRUCache(3, SeparateChainingHashTable)
    
    cache.put("user:123", {"name": "Alice", "email": "alice@example.com"})
    cache.put("user:456", {"name": "Bob", "email": "bob@example.com"})
    cache.put("user:789", {"name": "Charlie", "email": "charlie@example.com"})
    
    print(f"Cache after 3 inserts: {len(cache)} items")
    
    # Access an item to make it most recently used
    user = cache.get("user:123")
    print(f"Retrieved user: {user}")
    
    # Add another item, should evict least recently used
    cache.put("user:999", {"name": "David", "email": "david@example.com"})
    print(f"Cache after 4th insert: {len(cache)} items")
    print(f"Bob still in cache: {'user:456' in cache}")
    
    # 2. Symbol Table Demo
    print("\n2. SYMBOL TABLE DEMONSTRATION")
    print("-" * 40)
    symbol_table = SymbolTable(DoubleHashingHashTable)
    
    # Global scope
    symbol_table.insert("global_var", "variable", line_number=1, type_info="int")
    symbol_table.insert("global_func", "function", line_number=2, return_type="void")
    
    # Function scope
    symbol_table.enter_scope()
    symbol_table.insert("param", "parameter", line_number=5, type_info="string")
    symbol_table.insert("local_var", "variable", line_number=6, type_info="float")
    
    print(f"Current scope depth: {symbol_table.get_scope_depth()}")
    print(f"Lookup 'global_var': {symbol_table.lookup('global_var')}")
    print(f"Lookup 'param': {symbol_table.lookup('param')}")
    print(f"Lookup 'local_var' in current scope: {symbol_table.lookup_current_scope('local_var')}")
    
    symbol_table.exit_scope()
    print(f"After exit scope, depth: {symbol_table.get_scope_depth()}")
    
    # 3. Database Index Demo
    print("\n3. DATABASE INDEX DEMONSTRATION")
    print("-" * 40)
    db = DatabaseIndex(LinearProbingHashTable)
    
    # Insert some records
    db.insert_record(name="Alice", age=25, city="New York")
    db.insert_record(name="Bob", age=30, city="Los Angeles")
    db.insert_record(name="Charlie", age=25, city="Chicago")
    db.insert_record(name="David", age=35, city="New York")
    
    # Query using index
    ny_residents = db.find_by_field("city", "New York")
    print(f"New York residents: {ny_residents}")
    
    age_25 = db.find_by_field("age", 25)
    print(f"People aged 25: {age_25}")
    
    print(f"Database statistics: {db.get_index_statistics()}")
    
    # 4. Word Frequency Counter Demo
    print("\n4. WORD FREQUENCY COUNTER DEMONSTRATION")
    print("-" * 40)
    counter = WordFrequencyCounter(SeparateChainingHashTable)
    
    sample_text = """
    The quick brown fox jumps over the lazy dog. The fox is quick and brown.
    The dog is lazy and sleeps all day. The fox and dog are friends.
    """
    
    counter.add_text(sample_text)
    
    print(f"Most common words: {counter.get_most_common(5)}")
    print(f"Frequency of 'the': {counter.get_frequency('the')}")
    print(f"Probability of 'fox': {counter.get_word_probability('fox'):.3f}")
    print(f"Text statistics: {counter.get_statistics()}")
    
    # 5. Spell Checker Demo
    print("\n5. SPELL CHECKER DEMONSTRATION")
    print("-" * 40)
    
    # Simple dictionary
    dictionary = ["hello", "world", "python", "programming", "computer", "science", "algorithm"]
    spell_checker = SpellChecker(dictionary, QuadraticProbingHashTable)
    
    test_words = ["hello", "helo", "world", "worl", "python", "pythn"]
    
    for word in test_words:
        if spell_checker.is_correct(word):
            print(f"'{word}' is spelled correctly")
        else:
            suggestions = spell_checker.get_suggestions(word)
            print(f"'{word}' is misspelled. Suggestions: {suggestions}")
    
    print(f"Dictionary size: {spell_checker.get_dictionary_size()}")


if __name__ == "__main__":
    demonstrate_applications() 