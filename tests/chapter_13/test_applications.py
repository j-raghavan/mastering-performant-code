"""
Tests for real-world hash table applications.
"""

import pytest
import time
from src.chapter_13.applications import (
    LRUCache,
    SymbolTable,
    DatabaseIndex,
    WordFrequencyCounter,
    SpellChecker
)
from src.chapter_13.hash_table import (
    SeparateChainingHashTable,
    LinearProbingHashTable,
    QuadraticProbingHashTable,
    DoubleHashingHashTable
)


class TestLRUCache:
    """Test LRU Cache implementation."""
    
    def test_basic_operations(self):
        """Test basic cache operations."""
        cache = LRUCache(3, SeparateChainingHashTable)
        
        # Test put and get
        cache.put("key1", "value1")
        assert cache.get("key1") == "value1"
        assert len(cache) == 1
        
        # Test updating existing key
        cache.put("key1", "new_value1")
        assert cache.get("key1") == "new_value1"
        assert len(cache) == 1
        
        # Test multiple items
        cache.put("key2", "value2")
        cache.put("key3", "value3")
        assert len(cache) == 3
        assert cache.get("key2") == "value2"
        assert cache.get("key3") == "value3"
    
    def test_lru_eviction(self):
        """Test LRU eviction policy."""
        cache = LRUCache(2, LinearProbingHashTable)
        
        # Fill cache
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        assert len(cache) == 2
        
        # Access key1 to make it most recently used
        cache.get("key1")
        
        # Add new item, should evict key2 (least recently used)
        cache.put("key3", "value3")
        assert len(cache) == 2
        assert cache.get("key1") == "value1"  # Should still be there
        assert cache.get("key2") is None      # Should be evicted
        assert cache.get("key3") == "value3"  # Should be there
    
    def test_cache_statistics(self):
        """Test cache statistics."""
        cache = LRUCache(5, QuadraticProbingHashTable)
        
        cache.put("key1", "value1")
        cache.put("key2", "value2")
        
        stats = cache.get_statistics()
        assert stats['capacity'] == 5
        assert stats['size'] == 2
        assert stats['utilization'] == 2/5
        assert 'cache_stats' in stats
    
    def test_different_hash_table_implementations(self):
        """Test cache with different hash table implementations."""
        implementations = [
            SeparateChainingHashTable,
            LinearProbingHashTable,
            QuadraticProbingHashTable,
            DoubleHashingHashTable
        ]
        
        for impl in implementations:
            cache = LRUCache(3, impl)
            cache.put("key1", "value1")
            cache.put("key2", "value2")
            
            assert cache.get("key1") == "value1"
            assert cache.get("key2") == "value2"
            assert len(cache) == 2


class TestSymbolTable:
    """Test Symbol Table implementation."""
    
    def test_basic_operations(self):
        """Test basic symbol table operations."""
        symbol_table = SymbolTable(DoubleHashingHashTable)
        
        # Test insert and lookup
        symbol_table.insert("variable1", "variable", line_number=10, type_info="int")
        symbol_info = symbol_table.lookup("variable1")
        
        assert symbol_info is not None
        assert symbol_info['type'] == "variable"
        assert symbol_info['line_number'] == 10
        assert symbol_info['type_info'] == "int"
        assert symbol_info['scope'] == 0
    
    def test_scope_management(self):
        """Test scope entering and exiting."""
        symbol_table = SymbolTable(SeparateChainingHashTable)
        
        # Global scope
        assert symbol_table.get_scope_depth() == 0
        symbol_table.insert("global_var", "variable")
        
        # Enter function scope
        symbol_table.enter_scope()
        assert symbol_table.get_scope_depth() == 1
        symbol_table.insert("local_var", "variable")
        
        # Test lookup in current scope
        local_info = symbol_table.lookup_current_scope("local_var")
        assert local_info is not None
        assert local_info['scope'] == 1
        
        # Test lookup from inner scope (should find global)
        global_info = symbol_table.lookup("global_var")
        assert global_info is not None
        assert global_info['scope'] == 0
        
        # Exit scope
        symbol_table.exit_scope()
        assert symbol_table.get_scope_depth() == 0
        
        # Local var should not be accessible
        assert symbol_table.lookup("local_var") is None
    
    def test_symbol_attributes(self):
        """Test symbol attributes and metadata."""
        symbol_table = SymbolTable(LinearProbingHashTable)
        
        symbol_table.insert(
            "function1", 
            "function", 
            line_number=5, 
            return_type="void",
            parameters=["int", "string"],
            visibility="public"
        )
        
        symbol_info = symbol_table.lookup("function1")
        assert symbol_info['type'] == "function"
        assert symbol_info['return_type'] == "void"
        assert symbol_info['parameters'] == ["int", "string"]
        assert symbol_info['visibility'] == "public"
    
    def test_all_symbols_retrieval(self):
        """Test getting all symbols from all scopes."""
        symbol_table = SymbolTable(QuadraticProbingHashTable)
        
        symbol_table.insert("global1", "variable")
        symbol_table.insert("global2", "function")
        
        symbol_table.enter_scope()
        symbol_table.insert("local1", "variable")
        
        all_symbols = symbol_table.get_all_symbols()
        assert len(all_symbols) == 3
        assert "global1" in all_symbols
        assert "global2" in all_symbols
        assert "local1" in all_symbols


class TestDatabaseIndex:
    """Test Database Index implementation."""
    
    def test_basic_operations(self):
        """Test basic database index operations."""
        db = DatabaseIndex(LinearProbingHashTable)
        
        # Insert records
        id1 = db.insert_record(name="Alice", age=25, city="New York")
        id2 = db.insert_record(name="Bob", age=30, city="Los Angeles")
        
        assert id1 == 0
        assert id2 == 1
        
        # Query by field
        ny_residents = db.find_by_field("city", "New York")
        assert len(ny_residents) == 1
        assert ny_residents[0]['name'] == "Alice"
        
        age_30 = db.find_by_field("age", 30)
        assert len(age_30) == 1
        assert age_30[0]['name'] == "Bob"
    
    def test_multiple_matches(self):
        """Test queries that return multiple matches."""
        db = DatabaseIndex(SeparateChainingHashTable)
        
        db.insert_record(name="Alice", age=25, city="New York")
        db.insert_record(name="Bob", age=25, city="Chicago")
        db.insert_record(name="Charlie", age=30, city="New York")
        
        # Multiple people aged 25
        age_25 = db.find_by_field("age", 25)
        assert len(age_25) == 2
        names = {record['name'] for record in age_25}
        assert names == {"Alice", "Bob"}
        
        # Multiple people in New York
        ny_residents = db.find_by_field("city", "New York")
        assert len(ny_residents) == 2
        names = {record['name'] for record in ny_residents}
        assert names == {"Alice", "Charlie"}
    
    def test_record_deletion(self):
        """Test record deletion and index updates."""
        db = DatabaseIndex(DoubleHashingHashTable)
        
        id1 = db.insert_record(name="Alice", age=25, city="New York")
        id2 = db.insert_record(name="Bob", age=25, city="Chicago")
        
        # Verify records exist
        assert len(db.find_by_field("age", 25)) == 2
        
        # Delete one record
        assert db.delete_record(id1) is True
        
        # Verify deletion
        assert len(db.find_by_field("age", 25)) == 1
        assert len(db.find_by_field("city", "New York")) == 0
        
        # Try to delete non-existent record
        assert db.delete_record(999) is False
    
    def test_index_statistics(self):
        """Test index statistics."""
        db = DatabaseIndex(QuadraticProbingHashTable)
        
        db.insert_record(name="Alice", age=25, city="New York")
        db.insert_record(name="Bob", age=30, city="Los Angeles")
        
        stats = db.get_index_statistics()
        assert stats['total_records'] == 2
        assert stats['index_size'] > 0
        assert 'index_stats' in stats
        assert 'memory_info' in stats
    
    def test_all_records_retrieval(self):
        """Test getting all records."""
        db = DatabaseIndex(LinearProbingHashTable)
        
        db.insert_record(name="Alice", age=25)
        db.insert_record(name="Bob", age=30)
        
        all_records = db.get_all_records()
        assert len(all_records) == 2
        
        names = {record['name'] for record in all_records}
        assert names == {"Alice", "Bob"}


class TestWordFrequencyCounter:
    """Test Word Frequency Counter implementation."""
    
    def test_basic_counting(self):
        """Test basic word frequency counting."""
        counter = WordFrequencyCounter(SeparateChainingHashTable)
        
        text = "the quick brown fox jumps over the lazy dog"
        counter.add_text(text)
        
        assert counter.get_frequency("the") == 2
        assert counter.get_frequency("quick") == 1
        assert counter.get_frequency("nonexistent") == 0
    
    def test_case_insensitive(self):
        """Test that counting is case insensitive."""
        counter = WordFrequencyCounter(LinearProbingHashTable)
        
        counter.add_text("The Quick Brown Fox")
        counter.add_text("the quick brown fox")
        
        assert counter.get_frequency("the") == 2
        assert counter.get_frequency("The") == 2
        assert counter.get_frequency("QUICK") == 2
    
    def test_most_common_words(self):
        """Test getting most common words."""
        counter = WordFrequencyCounter(DoubleHashingHashTable)
        
        text = "the quick brown fox jumps over the lazy dog the fox is quick"
        counter.add_text(text)
        
        most_common = counter.get_most_common(3)
        assert len(most_common) == 3
        
        # Check that 'the' appears most frequently
        assert most_common[0][0] == "the"
        assert most_common[0][1] == 3
    
    def test_word_probability(self):
        """Test word probability calculation."""
        counter = WordFrequencyCounter(QuadraticProbingHashTable)
        
        text = "the quick brown fox"
        counter.add_text(text)
        
        # 4 words total, each appears once
        assert counter.get_word_probability("the") == 0.25
        assert counter.get_word_probability("quick") == 0.25
        assert counter.get_word_probability("nonexistent") == 0.0
    
    def test_statistics(self):
        """Test text statistics."""
        counter = WordFrequencyCounter(SeparateChainingHashTable)
        
        text = "the quick brown fox jumps over the lazy dog"
        counter.add_text(text)
        
        stats = counter.get_statistics()
        assert stats['total_words'] == 9
        assert stats['unique_words'] == 8
        assert stats['average_frequency'] > 0
        assert 'frequency_stats' in stats
    
    def test_multiple_text_additions(self):
        """Test adding multiple text segments."""
        counter = WordFrequencyCounter(LinearProbingHashTable)
        
        counter.add_text("the quick brown")
        counter.add_text("fox jumps over")
        counter.add_text("the lazy dog")
        
        assert counter.get_frequency("the") == 2
        assert counter.get_total_words() == 9


class TestSpellChecker:
    """Test Spell Checker implementation."""
    
    def test_basic_spell_checking(self):
        """Test basic spell checking functionality."""
        dictionary = ["hello", "world", "python", "programming"]
        spell_checker = SpellChecker(dictionary, SeparateChainingHashTable)
        
        assert spell_checker.is_correct("hello") is True
        assert spell_checker.is_correct("world") is True
        assert spell_checker.is_correct("helo") is False
        assert spell_checker.is_correct("nonexistent") is False
    
    def test_case_insensitive_checking(self):
        """Test case insensitive spell checking."""
        dictionary = ["Hello", "World", "Python"]
        spell_checker = SpellChecker(dictionary, LinearProbingHashTable)
        
        assert spell_checker.is_correct("hello") is True
        assert spell_checker.is_correct("HELLO") is True
        assert spell_checker.is_correct("Hello") is True
    
    def test_spelling_suggestions(self):
        """Test spelling suggestion functionality."""
        dictionary = ["hello", "world", "python", "programming", "computer"]
        spell_checker = SpellChecker(dictionary, DoubleHashingHashTable)
        
        # Test suggestions for misspelled words
        suggestions = spell_checker.get_suggestions("helo")
        assert len(suggestions) > 0
        assert "hello" in suggestions
        
        suggestions = spell_checker.get_suggestions("pythn")
        assert len(suggestions) > 0
        assert "python" in suggestions
    
    def test_no_suggestions_for_correct_words(self):
        """Test that correct words don't get suggestions."""
        dictionary = ["hello", "world"]
        spell_checker = SpellChecker(dictionary, QuadraticProbingHashTable)
        
        suggestions = spell_checker.get_suggestions("hello")
        assert len(suggestions) == 0
    
    def test_edit_distance_calculation(self):
        """Test edit distance calculation."""
        dictionary = ["hello", "world"]
        spell_checker = SpellChecker(dictionary, SeparateChainingHashTable)
        
        # Test edit distance method directly
        assert spell_checker._edit_distance("hello", "helo") == 1
        assert spell_checker._edit_distance("hello", "world") == 4
        assert spell_checker._edit_distance("", "hello") == 5
        assert spell_checker._edit_distance("hello", "") == 5
        assert spell_checker._edit_distance("hello", "hello") == 0
    
    def test_dictionary_size(self):
        """Test dictionary size tracking."""
        dictionary = ["hello", "world", "python", "programming"]
        spell_checker = SpellChecker(dictionary, LinearProbingHashTable)
        
        assert spell_checker.get_dictionary_size() == 4
    
    def test_suggestion_limit(self):
        """Test that suggestions respect the limit."""
        dictionary = ["hello", "world", "python", "programming", "computer", "science"]
        spell_checker = SpellChecker(dictionary, DoubleHashingHashTable)
        
        suggestions = spell_checker.get_suggestions("test", max_suggestions=3)
        assert len(suggestions) <= 3


def test_demonstrate_applications():
    """Test the demonstration function runs without errors."""
    from src.chapter_13.applications import demonstrate_applications
    
    # This should run without raising exceptions
    try:
        demonstrate_applications()
    except Exception as e:
        pytest.fail(f"demonstrate_applications() raised {e} unexpectedly!") 