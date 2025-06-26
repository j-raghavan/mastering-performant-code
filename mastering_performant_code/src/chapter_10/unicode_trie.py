"""
Unicode Trie Implementation

This module provides a Unicode-aware trie implementation that handles
Unicode normalization, case folding, and proper character comparison.
"""

import unicodedata
from typing import TypeVar, Generic, Optional, List, Tuple
from src.chapter_10.trie import Trie, TrieNode

T = TypeVar('T')

class UnicodeTrie(Trie[T]):
    """
    A Unicode-aware trie implementation.
    
    This trie handles Unicode normalization, case folding, and
    proper character comparison for international text.
    """
    
    def __init__(self, normalize: bool = True, case_sensitive: bool = True) -> None:
        """
        Initialize a Unicode-aware trie.
        
        Args:
            normalize: Whether to normalize Unicode strings (NFC)
            case_sensitive: Whether to preserve case
        """
        super().__init__()
        self._normalize = normalize
        self._case_sensitive = case_sensitive
    
    def _normalize_string(self, s: str) -> str:
        """Normalize a string according to trie settings."""
        if self._normalize:
            s = unicodedata.normalize('NFC', s)
        if not self._case_sensitive:
            s = s.casefold()
        return s
    
    def insert(self, key: str, value: Optional[T] = None) -> None:
        """Insert a Unicode string into the trie."""
        normalized_key = self._normalize_string(key)
        super().insert(normalized_key, value)
    
    def search(self, key: str) -> Optional[T]:
        """Search for a Unicode string in the trie."""
        normalized_key = self._normalize_string(key)
        return super().search(normalized_key)
    
    def starts_with(self, prefix: str) -> bool:
        """Check if any string starts with the given Unicode prefix."""
        normalized_prefix = self._normalize_string(prefix)
        return super().starts_with(normalized_prefix)
    
    def get_all_with_prefix(self, prefix: str) -> List[Tuple[str, T]]:
        """Get all strings with the given Unicode prefix."""
        normalized_prefix = self._normalize_string(prefix)
        return super().get_all_with_prefix(normalized_prefix)
    
    def autocomplete(self, prefix: str, max_results: int = 10) -> List[str]:
        """Get autocomplete suggestions for a Unicode prefix."""
        normalized_prefix = self._normalize_string(prefix)
        return super().autocomplete(normalized_prefix, max_results)
    
    def delete(self, key: str) -> bool:
        """Delete a Unicode string from the trie."""
        normalized_key = self._normalize_string(key)
        return super().delete(normalized_key)
    
    def __contains__(self, key: str) -> bool:
        """Check if a Unicode string is stored in the trie."""
        normalized_key = self._normalize_string(key)
        return super().__contains__(normalized_key)
    
    def __getitem__(self, key: str) -> T:
        """Get the value associated with a Unicode key."""
        normalized_key = self._normalize_string(key)
        return super().__getitem__(normalized_key)
    
    def __setitem__(self, key: str, value: T) -> None:
        """Set the value associated with a Unicode key."""
        normalized_key = self._normalize_string(key)
        super().__setitem__(normalized_key, value)
    
    def __delitem__(self, key: str) -> None:
        """Remove a Unicode key from the trie."""
        normalized_key = self._normalize_string(key)
        super().__delitem__(normalized_key) 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running unicode_trie demonstration...")
    print("=" * 50)

    # Create instance of UnicodeTrie
    try:
        instance = UnicodeTrie()
        print(f"✓ Created UnicodeTrie instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating UnicodeTrie instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
