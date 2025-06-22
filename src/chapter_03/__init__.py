"""
Chapter 3: Dynamic Array with Manual Resizing

This module contains implementations of dynamic arrays with different growth strategies,
performance analysis tools, and real-world applications.
"""

from .dynamic_array import (
    DynamicArray,
    AdvancedDynamicArray,
    ProductionDynamicArray,
    GrowthStrategy
)

from .applications import (
    TextBuffer,
    DatabaseRecord,
    SimpleDatabase
)

from .benchmarks import (
    benchmark_growth_strategies,
    compare_with_builtin_list,
    analyze_amortized_complexity
)

__all__ = [
    'DynamicArray',
    'AdvancedDynamicArray', 
    'ProductionDynamicArray',
    'GrowthStrategy',
    'TextBuffer',
    'DatabaseRecord',
    'SimpleDatabase',
    'benchmark_growth_strategies',
    'compare_with_builtin_list',
    'analyze_amortized_complexity'
] 