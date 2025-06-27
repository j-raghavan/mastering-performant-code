"""
Real-World Applications of Bloom Filters

This module provides practical applications demonstrating how Bloom filters
can be used in real-world scenarios.
"""

import timeit
from typing import Any, List, Optional, Tuple, Dict, Set
from .bloom_filter import BloomFilter
from .analyzer import BloomFilterAnalyzer

class SpellChecker:
    """
    Real-world application: Spell checker using Bloom filter.
    
    This demonstrates how Bloom filters can be used for efficient
    spell checking with a dictionary of known words.
    """
    
    def __init__(self, dictionary_words: List[str], false_positive_rate: float = 0.01):
        """
        Initialize spell checker with dictionary.
        
        Args:
            dictionary_words: List of correctly spelled words
            false_positive_rate: Desired false positive rate
        """
        self.dictionary_words = dictionary_words
        self.bloom_filter = BloomFilter(
            expected_elements=len(dictionary_words),
            false_positive_rate=false_positive_rate
        )
        
        # Add all dictionary words to Bloom filter
        for word in dictionary_words:
            self.bloom_filter.add(word.lower())
    
    def is_correctly_spelled(self, word: str) -> bool:
        """
        Check if a word is correctly spelled.
        
        Args:
            word: Word to check
            
        Returns:
            True if word is probably correctly spelled
        """
        return self.bloom_filter.contains(word.lower())
    
    def check_text(self, text: str) -> List[Tuple[str, int, bool]]:
        """
        Check spelling in a text.
        
        Args:
            text: Text to check
            
        Returns:
            List of (word, position, is_correct) tuples
        """
        words = text.split()
        results = []
        
        for i, word in enumerate(words):
            # Remove punctuation for checking
            clean_word = ''.join(c for c in word if c.isalpha())
            if clean_word:
                is_correct = self.is_correctly_spelled(clean_word)
                results.append((word, i, is_correct))
        
        return results
    
    def get_suggestions(self, misspelled_word: str, max_suggestions: int = 5) -> List[str]:
        """
        Get spelling suggestions for a misspelled word.
        
        This is a simplified implementation that returns words from the dictionary
        that are similar in length. In a real implementation, you would use
        edit distance algorithms.
        
        Args:
            misspelled_word: Word to get suggestions for
            max_suggestions: Maximum number of suggestions to return
            
        Returns:
            List of suggested words
        """
        word_len = len(misspelled_word)
        suggestions = []
        
        for word in self.dictionary_words:
            if abs(len(word) - word_len) <= 2:  # Similar length
                suggestions.append(word)
                if len(suggestions) >= max_suggestions:
                    break
        
        return suggestions
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get spell checker statistics.
        
        Returns:
            Dictionary with spell checker statistics
        """
        return {
            'dictionary_size': len(self.dictionary_words),
            'bloom_filter_stats': BloomFilterAnalyzer.analyze_bloom_filter(self.bloom_filter),
            'memory_efficiency': self.bloom_filter.get_memory_usage() / (len(self.dictionary_words) * 8)
        }

class WebCache:
    """
    Real-world application: Web cache using Bloom filter.
    
    This demonstrates how Bloom filters can be used to efficiently
    check if a URL has been cached without storing the full URL.
    """
    
    def __init__(self, expected_urls: int, false_positive_rate: float = 0.01):
        """
        Initialize web cache with Bloom filter.
        
        Args:
            expected_urls: Expected number of URLs to cache
            false_positive_rate: Desired false positive rate
        """
        self.bloom_filter = BloomFilter(
            expected_elements=expected_urls,
            false_positive_rate=false_positive_rate
        )
        self.cache_hits = 0
        self.cache_misses = 0
        self.false_positives = 0
        self.total_requests = 0
    
    def add_url(self, url: str) -> None:
        """
        Add a URL to the cache.
        
        Args:
            url: URL to add to cache
        """
        self.bloom_filter.add(url)
    
    def is_cached(self, url: str) -> bool:
        """
        Check if a URL is cached.
        
        Args:
            url: URL to check
            
        Returns:
            True if URL is probably cached
        """
        return self.bloom_filter.contains(url)
    
    def simulate_cache_access(self, url: str, actually_cached: bool) -> str:
        """
        Simulate cache access with tracking.
        
        Args:
            url: URL to check
            actually_cached: Whether URL is actually in cache
            
        Returns:
            'hit', 'miss', or 'false_positive'
        """
        self.total_requests += 1
        bloom_result = self.is_cached(url)
        
        if actually_cached:
            if bloom_result:
                self.cache_hits += 1
                return 'hit'
            else:
                self.cache_misses += 1
                return 'miss'
        else:
            if bloom_result:
                self.false_positives += 1
                return 'false_positive'
            else:
                self.cache_misses += 1
                return 'miss'
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get cache performance statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        if self.total_requests == 0:
            return {
                'hit_rate': 0.0,
                'miss_rate': 0.0,
                'false_positive_rate': 0.0,
                'total_requests': 0,
                'cache_hits': 0,
                'cache_misses': 0,
                'false_positives': 0
            }
        
        return {
            'hit_rate': self.cache_hits / self.total_requests,
            'miss_rate': self.cache_misses / self.total_requests,
            'false_positive_rate': self.false_positives / self.total_requests,
            'total_requests': self.total_requests,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'false_positives': self.false_positives,
            'bloom_filter_stats': BloomFilterAnalyzer.analyze_bloom_filter(self.bloom_filter)
        }
    
    def reset_stats(self) -> None:
        """Reset cache statistics."""
        self.cache_hits = 0
        self.cache_misses = 0
        self.false_positives = 0
        self.total_requests = 0

class DuplicateDetector:
    """
    Real-world application: Duplicate detection using Bloom filter.
    
    This demonstrates how Bloom filters can be used to efficiently
    detect duplicate items in a stream of data.
    """
    
    def __init__(self, expected_items: int, false_positive_rate: float = 0.01):
        """
        Initialize duplicate detector.
        
        Args:
            expected_items: Expected number of unique items
            false_positive_rate: Desired false positive rate
        """
        self.bloom_filter = BloomFilter(
            expected_elements=expected_items,
            false_positive_rate=false_positive_rate
        )
        self.total_items = 0
        self.duplicates_found = 0
        self.false_duplicates = 0
    
    def process_item(self, item: Any) -> bool:
        """
        Process an item and check if it's a duplicate.
        
        Args:
            item: Item to process
            
        Returns:
            True if item is probably a duplicate, False if definitely new
        """
        self.total_items += 1
        
        if self.bloom_filter.contains(item):
            self.duplicates_found += 1
            return True
        else:
            self.bloom_filter.add(item)
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get duplicate detection statistics.
        
        Returns:
            Dictionary with detection statistics
        """
        unique_items = len(self.bloom_filter)
        actual_duplicates = self.total_items - unique_items
        
        return {
            'total_items': self.total_items,
            'unique_items': unique_items,
            'duplicates_found': self.duplicates_found,
            'actual_duplicates': actual_duplicates,
            'false_duplicates': self.duplicates_found - actual_duplicates,
            'duplicate_rate': self.duplicates_found / max(1, self.total_items),
            'bloom_filter_stats': BloomFilterAnalyzer.analyze_bloom_filter(self.bloom_filter)
        }

class EmailFilter:
    """
    Real-world application: Email filtering using Bloom filter.
    
    This demonstrates how Bloom filters can be used to efficiently
    filter spam emails based on known spam patterns.
    """
    
    def __init__(self, spam_patterns: List[str], false_positive_rate: float = 0.01):
        """
        Initialize email filter with spam patterns.
        
        Args:
            spam_patterns: List of known spam patterns/words
            false_positive_rate: Desired false positive rate
        """
        self.spam_patterns = spam_patterns
        self.bloom_filter = BloomFilter(
            expected_elements=len(spam_patterns),
            false_positive_rate=false_positive_rate
        )
        
        # Add spam patterns to Bloom filter
        for pattern in spam_patterns:
            self.bloom_filter.add(pattern.lower())
        
        self.emails_processed = 0
        self.spam_detected = 0
        self.false_positives = 0
    
    def is_spam(self, email_content: str) -> bool:
        """
        Check if an email is spam.
        
        Args:
            email_content: Email content to check
            
        Returns:
            True if email is probably spam
        """
        self.emails_processed += 1
        
        # Extract words from email content
        words = email_content.lower().split()
        
        # Check if any spam patterns are present
        spam_patterns_found = sum(1 for word in words if self.bloom_filter.contains(word))
        
        # Consider email spam if multiple patterns are found
        is_spam = spam_patterns_found >= 2
        
        if is_spam:
            self.spam_detected += 1
        
        return is_spam
    
    def simulate_email_processing(self, emails: List[Tuple[str, bool]]) -> Dict[str, Any]:
        """
        Simulate processing a list of emails with known spam status.
        
        Args:
            emails: List of (email_content, is_actually_spam) tuples
            
        Returns:
            Dictionary with processing results
        """
        results = {
            'correct_spam_detections': 0,
            'false_spam_detections': 0,
            'missed_spam': 0,
            'correct_ham_detections': 0
        }
        
        for email_content, is_actually_spam in emails:
            detected_as_spam = self.is_spam(email_content)
            
            if is_actually_spam:
                if detected_as_spam:
                    results['correct_spam_detections'] += 1
                else:
                    results['missed_spam'] += 1
            else:
                if detected_as_spam:
                    results['false_spam_detections'] += 1
                else:
                    results['correct_ham_detections'] += 1
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get email filter statistics.
        
        Returns:
            Dictionary with filter statistics
        """
        return {
            'emails_processed': self.emails_processed,
            'spam_detected': self.spam_detected,
            'spam_detection_rate': self.spam_detected / max(1, self.emails_processed),
            'spam_patterns': len(self.spam_patterns),
            'bloom_filter_stats': BloomFilterAnalyzer.analyze_bloom_filter(self.bloom_filter)
        }

class URLShortener:
    """
    Real-world application: URL shortener using Bloom filter.
    
    This demonstrates how Bloom filters can be used to efficiently
    detect duplicate URLs in a URL shortening service.
    """
    
    def __init__(self, expected_urls: int, false_positive_rate: float = 0.01):
        """
        Initialize URL shortener.
        
        Args:
            expected_urls: Expected number of unique URLs
            false_positive_rate: Desired false positive rate
        """
        self.bloom_filter = BloomFilter(
            expected_elements=expected_urls,
            false_positive_rate=false_positive_rate
        )
        self.url_mappings = {}  # short_url -> original_url
        self.urls_processed = 0
        self.duplicates_found = 0
    
    def shorten_url(self, original_url: str) -> str:
        """
        Shorten a URL, checking for duplicates.
        
        Args:
            original_url: Original URL to shorten
            
        Returns:
            Shortened URL
        """
        self.urls_processed += 1
        
        # Check if URL already exists
        if self.bloom_filter.contains(original_url):
            self.duplicates_found += 1
            # In a real implementation, you would return the existing short URL
            return f"duplicate_{hash(original_url) % 10000}"
        
        # Add URL to Bloom filter
        self.bloom_filter.add(original_url)
        
        # Generate short URL
        short_url = f"short_{hash(original_url) % 10000}"
        self.url_mappings[short_url] = original_url
        
        return short_url
    
    def get_original_url(self, short_url: str) -> Optional[str]:
        """
        Get original URL from short URL.
        
        Args:
            short_url: Shortened URL
            
        Returns:
            Original URL if found, None otherwise
        """
        return self.url_mappings.get(short_url)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get URL shortener statistics.
        
        Returns:
            Dictionary with shortener statistics
        """
        return {
            'urls_processed': self.urls_processed,
            'unique_urls': len(self.bloom_filter),
            'duplicates_found': self.duplicates_found,
            'duplicate_rate': self.duplicates_found / max(1, self.urls_processed),
            'short_urls_generated': len(self.url_mappings),
            'bloom_filter_stats': BloomFilterAnalyzer.analyze_bloom_filter(self.bloom_filter)
        } 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running applications demonstration...")
    print("=" * 50)

    # Create instance of SpellChecker
    try:
        instance = SpellChecker()
        print(f"✓ Created SpellChecker instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating SpellChecker instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
