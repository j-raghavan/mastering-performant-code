[![Tests](https://github.com/yourusername/mastering-performant-code/workflows/Run%20Tests/badge.svg)](https://github.com/yourusername/mastering-performant-code/actions)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Mastering Performant Code

A comprehensive companion repository for the book "Mastering Performant Code" - your journey into Python performance optimization, data structures, and algorithmic efficiency.

## 🚀 Overview

This repository contains hands-on implementations, examples, and exercises that accompany the book "Mastering Performant Code". Each chapter focuses on specific performance concepts, data structures, and optimization techniques using only Python 3.12's standard library.

## 🐍 Requirements

- **Python 3.12+** (minimum requirement)
- No external dependencies - everything uses Python's standard library
- Compatible with Linux, macOS, and Windows

## 📚 Chapter Overview

### Chapter 1: Built-ins Under the Hood
**Topics:** Python's core data structures, memory management, performance analysis
- Dynamic Array implementation with memory tracking
- Hash Table with collision resolution
- Simple Set implementation
- Configuration management system
- Built-in analyzer for performance comparison

### Chapter 2: Algorithmic Complexity & Profiling Techniques
**Topics:** Big O notation, profiling tools, benchmarking
- Performance and memory profilers
- Complexity analysis tools
- Multiple algorithm implementations (sum, fibonacci)
- Comprehensive benchmarking suite
- Real-world performance comparison

### Chapter 3: Dynamic Array with Manual Resizing
**Topics:** Amortized analysis, growth strategies, real-world applications
- Multiple growth strategy implementations
- Text buffer and database applications
- Amortized complexity analysis
- Performance comparison with built-in list

### Chapter 4: Linked Lists & Iterator Protocol
**Topics:** Linked list implementations, iterator design, memory efficiency
- Singly and doubly linked lists
- Advanced iterator with state management
- Undo/Redo system implementation
- Memory and performance analysis tools

### Chapter 5: Advanced Data Structures
**Topics:** Priority queues, skip lists, task scheduling
- Priority queue implementations
- Skip list data structure
- Task scheduler application
- Performance analysis and optimization

### Chapter 6: Binary Search Trees
**Topics:** Tree structures, file system organization, search optimization
- Recursive and iterative BST implementations
- File system tree application
- BST node management
- Performance analysis tools

### Chapter 7: Self-Balancing Trees (AVL)
**Topics:** Tree balancing, database indexing, height management
- AVL tree implementation with rotation
- Database indexing application
- Height-balanced tree maintenance
- Performance analysis

### Chapter 8: Red-Black Trees
**Topics:** Advanced balancing, real-world applications
- Complete Red-Black tree implementation
- Real-world applications and use cases
- Performance characteristics

### Chapter 9: B-Trees
**Topics:** Disk-based data structures, database optimization
- B-tree implementation for disk storage
- Database indexing with B-trees
- Node management and splitting
- Performance analysis

### Chapter 10: Trie & Compressed Trie
**Topics:** String processing, autocomplete, spell checking
- Standard and compressed trie implementations
- Unicode-aware trie
- Autocomplete system
- Spell checker application
- Performance benchmarking

### Chapter 11: Heaps & Priority Queues
**Topics:** Heap data structure, sorting, priority management
- Binary heap implementation
- Heap sort algorithm
- Priority queue with heap backing
- Real-world applications

### Chapter 12: Union-Find (Disjoint Sets)
**Topics:** Graph algorithms, network connectivity, image processing
- Multiple disjoint set implementations
- Network connectivity analysis
- Image segmentation application
- Memory tracking and optimization

### Chapter 13: Advanced Hash Tables
**Topics:** Hash table optimization, collision resolution, performance tuning
- Advanced hash table implementations
- Real-world applications
- Performance benchmarking

### Chapter 14: Bloom Filters
**Topics:** Probabilistic data structures, memory efficiency, false positives
- Standard and counting bloom filters
- Scalable bloom filter implementation
- Real-world applications
- Performance analysis

### Chapter 15: Caching Strategies
**Topics:** LRU/LFU caches, memory management, performance optimization
- LRU cache implementation
- LFU cache implementation
- Performance analyzer
- Real-world caching applications

### Chapter 16: Integration Patterns & Memory Management
**Topics:** Design patterns, memory profiling, object pooling
- Integration patterns for data structures
- Memory profiling tools
- Object pool implementation
- Comprehensive demonstrations

## 🛠️ Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/mastering-performant-code.git
   cd mastering-performant-code
   ```

2. **Verify Python version:**
   ```bash
   python --version  # Should be 3.12+
   ```

3. **Run examples:**
   ```bash
   # Run a specific chapter demo
   python -m src.chapter_01.demo
   
   # Run all benchmarks
   python -m src.chapter_02.benchmarks
   ```

4. **Run tests:**
   ```bash
   # Run all tests
   pytest
   
   # Run tests for a specific chapter
   pytest tests/chapter_01/
   ```

## 📖 How to Use This Repository

### For Readers
- Each chapter contains `demo.py` files with comprehensive examples
- Run the demos to see concepts in action
- Use the analyzer tools to understand performance characteristics
- Experiment with the implementations to deepen your understanding

### For Educators
- Use the implementations as teaching examples
- Leverage the benchmarking tools for performance comparisons
- Assign exercises based on the provided data structures
- Use the test suite to validate student implementations

### For Developers
- Study the implementations for production-ready patterns
- Use the profiling tools in your own projects
- Adapt the data structures for your specific use cases
- Learn from the real-world applications provided

## 🧪 Testing

The repository includes comprehensive tests for each chapter:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test categories
pytest -k "test_performance"
pytest -k "test_memory"
```

## 📊 Performance Analysis

Each chapter includes tools for analyzing:
- **Time Complexity:** Big O analysis and benchmarking
- **Memory Usage:** Memory profiling and optimization
- **Real-world Performance:** Practical application testing
- **Scalability:** Performance under different data sizes

## 🤝 Contributing

While this is primarily a companion repository for the book, contributions are welcome:
- Bug fixes and improvements
- Additional examples and applications
- Performance optimizations
- Documentation enhancements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📖 Book Information

This repository accompanies "Mastering Performant Code" - a comprehensive guide to writing efficient, scalable Python applications. The book covers:

- Performance profiling and optimization techniques
- Data structure design and implementation
- Algorithmic complexity analysis
- Real-world performance considerations
- Memory management and efficiency

## 🎯 Key Learning Outcomes

By working through this repository, you'll gain:
- Deep understanding of Python's performance characteristics
- Hands-on experience with data structure implementations
- Proficiency in performance profiling and optimization
- Ability to choose the right data structures for specific problems
- Skills to write performant, scalable Python code

---

**Happy coding and optimizing! 🚀**

*Remember: The best optimization is the one you don't need to make.*
