"""
Test runner for Chapter 10: Trie & Compressed Trie

This script runs all unit tests for the trie implementations and provides
a summary of test results and performance metrics.
"""

import unittest
import sys
import os
import time
from typing import List, Dict, Any

# Add the project root to the path for imports
sys.path.insert(0, '../../')

def run_all_tests() -> Dict[str, Any]:
    """Run all tests and return results."""
    # Import all test modules
    from tests.chapter_10.test_trie import TestTrie, TestTrieNode, TestTriePerformance, TestTrieEdgeCases
    from tests.chapter_10.test_compressed_trie import TestCompressedTrie, TestCompressedTrieNode, TestCompressedTrieCompression, TestCompressedTriePerformance, TestCompressedTrieEdgeCases
    from tests.chapter_10.test_unicode_trie import TestUnicodeTrie, TestUnicodeTriePerformance
    from tests.chapter_10.test_autocomplete import TestAutocompleteSystem
    from tests.chapter_10.test_spell_checker import TestSpellChecker, TestSpellCheckerEdgeCases, TestSpellCheckerPerformance
    from tests.chapter_10.test_analyzer import TestTrieStats, TestTrieAnalyzer
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        # Trie tests
        TestTrieNode,
        TestTrie,
        TestTriePerformance,
        TestTrieEdgeCases,
        
        # Compressed Trie tests
        TestCompressedTrieNode,
        TestCompressedTrie,
        TestCompressedTrieCompression,
        TestCompressedTriePerformance,
        TestCompressedTrieEdgeCases,
        
        # Unicode Trie tests
        TestUnicodeTrie,
        TestUnicodeTriePerformance,
        
        # Application tests
        TestAutocompleteSystem,
        TestSpellChecker,
        TestSpellCheckerEdgeCases,
        TestSpellCheckerPerformance,
        
        # Analyzer tests
        TestTrieStats,
        TestTrieAnalyzer,
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    start_time = time.time()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    end_time = time.time()
    
    return {
        'tests_run': result.testsRun,
        'failures': len(result.failures),
        'errors': len(result.errors),
        'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0,
        'time_taken': end_time - start_time,
        'success': result.wasSuccessful(),
        'failure_details': result.failures,
        'error_details': result.errors
    }

def run_demo_tests() -> None:
    """Run demo tests to verify functionality."""
    print("\n" + "="*60)
    print("RUNNING DEMO TESTS")
    print("="*60)
    
    try:
        from src.chapter_10.trie import Trie
        from src.chapter_10.compressed_trie import CompressedTrie
        from src.chapter_10.unicode_trie import UnicodeTrie
        from src.chapter_10.autocomplete import AutocompleteSystem
        from src.chapter_10.spell_checker import SpellChecker
        from src.chapter_10.analyzer import TrieAnalyzer
        
        # Test basic trie functionality
        print("\n1. Testing Standard Trie:")
        trie = Trie()
        trie.insert("hello", "world")
        trie.insert("hi", "there")
        trie.insert("help", "me")
        
        print(f"   - Size: {len(trie)}")
        print(f"   - 'hello' in trie: {trie.search('hello')}")
        print(f"   - 'hi' in trie: {trie.search('hi')}")
        print(f"   - Prefix 'hel': {trie.starts_with('hel')}")
        print(f"   - Autocomplete 'hel': {trie.autocomplete('hel')}")
        
        # Test compressed trie
        print("\n2. Testing Compressed Trie:")
        comp_trie = CompressedTrie()
        comp_trie.insert("hello", "world")
        comp_trie.insert("help", "me")
        
        print(f"   - Size: {len(comp_trie)}")
        print(f"   - 'hello' in trie: {comp_trie.search('hello')}")
        print(f"   - 'help' in trie: {comp_trie.search('help')}")
        
        # Test Unicode trie
        print("\n3. Testing Unicode Trie:")
        unicode_trie = UnicodeTrie(case_sensitive=False)
        unicode_trie.insert("café", "coffee")
        unicode_trie.insert("CAFE", "coffee2")
        
        print(f"   - 'cafe' in trie: {unicode_trie.search('cafe')}")
        print(f"   - 'CAFE' in trie: {unicode_trie.search('CAFE')}")
        
        # Test autocomplete system
        print("\n4. Testing Autocomplete System:")
        autocomplete = AutocompleteSystem()
        autocomplete.add_word("python", 100)
        autocomplete.add_word("programming", 80)
        autocomplete.add_word("data", 90)
        
        suggestions = autocomplete.get_suggestions("pro", max_results=2)
        print(f"   - Suggestions for 'pro': {suggestions}")
        
        # Test spell checker
        print("\n5. Testing Spell Checker:")
        spell_checker = SpellChecker(["python", "programming", "data"])
        
        print(f"   - 'python' correct: {spell_checker.is_correct('python')}")
        print(f"   - 'pythn' correct: {spell_checker.is_correct('pythn')}")
        suggestions = spell_checker.get_suggestions("pythn", max_suggestions=2)
        print(f"   - Suggestions for 'pythn': {suggestions}")
        
        # Test analyzer
        print("\n6. Testing Trie Analyzer:")
        analyzer = TrieAnalyzer()
        stats = analyzer.analyze_trie(trie)
        print(f"   - Trie nodes: {stats.num_nodes}")
        print(f"   - Trie strings: {stats.num_strings}")
        print(f"   - Memory usage: {stats.memory_bytes} bytes")
        
        print("\n✅ All demo tests passed!")
        
    except Exception as e:
        print(f"\n❌ Demo test failed: {e}")
        import traceback
        traceback.print_exc()

def print_test_summary(results: Dict[str, Any]) -> None:
    """Print a summary of test results."""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    print(f"Tests Run: {results['tests_run']}")
    print(f"Failures: {results['failures']}")
    print(f"Errors: {results['errors']}")
    print(f"Skipped: {results['skipped']}")
    print(f"Time Taken: {results['time_taken']:.2f} seconds")
    print(f"Success: {'✅ PASSED' if results['success'] else '❌ FAILED'}")
    
    if results['failures']:
        print(f"\nFailures ({results['failures']}):")
        for test, traceback in results['failure_details']:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if results['errors']:
        print(f"\nErrors ({results['errors']}):")
        for test, traceback in results['error_details']:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")

def main():
    """Main function to run all tests."""
    print("Chapter 10: Trie & Compressed Trie - Test Suite")
    print("="*60)
    
    # Run demo tests first
    run_demo_tests()
    
    # Run unit tests
    print("\n" + "="*60)
    print("RUNNING UNIT TESTS")
    print("="*60)
    
    results = run_all_tests()
    
    # Print summary
    print_test_summary(results)
    
    # Exit with appropriate code
    if results['success']:
        print("\n🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        print(f"\n💥 {results['failures'] + results['errors']} test(s) failed!")
        sys.exit(1)

if __name__ == '__main__':
    main() 