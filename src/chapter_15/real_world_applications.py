"""
Real-world cache applications demonstrating practical usage.

This module provides realistic implementations of cache usage in
web applications, database systems, and other real-world scenarios.
"""

import time
import random
import hashlib
import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from .lru_cache import LRUCacheOrderedDict, LRUCacheDLL
from .lfu_cache import LFUCache

@dataclass
class CacheItem:
    """Generic cache item with metadata."""
    data: Any
    timestamp: float
    access_count: int = 0
    size: int = 0
    
    def update_access(self):
        """Update access statistics."""
        self.access_count += 1
        self.timestamp = time.time()
    
    def get_age(self) -> float:
        """Get age of the item in seconds."""
        return time.time() - self.timestamp

class WebPageCache:
    """Realistic web page caching system."""
    
    def __init__(self, cache_type: str = "lru", capacity: int = 100, ttl: int = 3600):
        """
        Initialize web page cache.
        
        Args:
            cache_type: Type of cache ("lru", "lfu", "lru_dll")
            capacity: Maximum number of pages to cache
            ttl: Time to live in seconds (default: 1 hour)
        """
        if cache_type.lower() == "lru":
            self.cache = LRUCacheOrderedDict(capacity)
        elif cache_type.lower() == "lfu":
            self.cache = LFUCache(capacity)
        elif cache_type.lower() == "lru_dll":
            self.cache = LRUCacheDLL(capacity)
        else:
            raise ValueError("Cache type must be 'lru', 'lfu', or 'lru_dll'")
        
        self.cache_type = cache_type
        self.ttl = ttl
        self.stats = {
            'requests': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'backend_requests': 0,
            'expired_items': 0,
            'total_response_time': 0.0
        }
    
    def get_page(self, url: str, user_agent: str = None) -> Optional[str]:
        """
        Get page from cache or backend.
        
        Args:
            url: The URL to fetch
            user_agent: User agent string for cache key
            
        Returns:
            Page content or None if not found
        """
        start_time = time.time()
        self.stats['requests'] += 1
        
        # Create cache key (consider user agent for personalized content)
        cache_key = self._create_cache_key(url, user_agent)
        
        # Try cache first
        cached_item = self.cache.get(cache_key)
        if cached_item and not self._is_expired(cached_item):
            cached_item.update_access()
            self.stats['cache_hits'] += 1
            self.stats['total_response_time'] += time.time() - start_time
            return cached_item.data
        
        # Cache miss or expired
        self.stats['cache_misses'] += 1
        
        # Simulate backend request
        page_content = self._fetch_from_backend(url, user_agent)
        
        if page_content:
            self.stats['backend_requests'] += 1
            cache_item = CacheItem(
                data=page_content,
                timestamp=time.time(),
                size=len(page_content)
            )
            self.cache.put(cache_key, cache_item)
        
        self.stats['total_response_time'] += time.time() - start_time
        return page_content
    
    def _create_cache_key(self, url: str, user_agent: str = None) -> str:
        """Create a cache key from URL and user agent."""
        key_data = url
        if user_agent:
            key_data += f"|{user_agent}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_expired(self, cache_item: CacheItem) -> bool:
        """Check if cache item has expired."""
        if time.time() - cache_item.timestamp > self.ttl:
            self.stats['expired_items'] += 1
            return True
        return False
    
    def _fetch_from_backend(self, url: str, user_agent: str = None) -> str:
        """
        Simulate fetching page from backend.
        
        Args:
            url: The URL to fetch
            user_agent: User agent string
            
        Returns:
            Simulated page content
        """
        # Simulate network latency (10-50ms)
        time.sleep(random.uniform(0.01, 0.05))
        
        # Simulate different content based on URL
        if "home" in url.lower():
            content = f"""
            <html>
                <head><title>Home Page</title></head>
                <body>
                    <h1>Welcome to Our Website</h1>
                    <p>This is the home page content.</p>
                    <p>User Agent: {user_agent or 'Unknown'}</p>
                    <p>Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                </body>
            </html>
            """
        elif "product" in url.lower():
            content = f"""
            <html>
                <head><title>Product Page</title></head>
                <body>
                    <h1>Product Details</h1>
                    <p>Product information and details.</p>
                    <p>User Agent: {user_agent or 'Unknown'}</p>
                    <p>Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                </body>
            </html>
            """
        else:
            content = f"""
            <html>
                <head><title>Generic Page</title></head>
                <body>
                    <h1>Page Content</h1>
                    <p>Generic page content for {url}</p>
                    <p>User Agent: {user_agent or 'Unknown'}</p>
                    <p>Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
                </body>
            </html>
            """
        
        return content
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics."""
        avg_response_time = 0.0
        if self.stats['requests'] > 0:
            avg_response_time = self.stats['total_response_time'] / self.stats['requests']
        
        hit_ratio = 0.0
        if self.stats['requests'] > 0:
            hit_ratio = self.stats['cache_hits'] / self.stats['requests']
        
        return {
            **self.stats,
            'hit_ratio': hit_ratio,
            'avg_response_time': avg_response_time,
            'cache_size': len(self.cache),
            'cache_type': self.cache_type,
            'ttl': self.ttl
        }

class DatabaseQueryCache:
    """Database query caching system."""
    
    def __init__(self, cache_type: str = "lru", capacity: int = 1000, ttl: int = 1800):
        """
        Initialize database query cache.
        
        Args:
            cache_type: Type of cache ("lru", "lfu", "lru_dll")
            capacity: Maximum number of queries to cache
            ttl: Time to live in seconds (default: 30 minutes)
        """
        if cache_type.lower() == "lru":
            self.cache = LRUCacheOrderedDict(capacity)
        elif cache_type.lower() == "lfu":
            self.cache = LFUCache(capacity)
        elif cache_type.lower() == "lru_dll":
            self.cache = LRUCacheDLL(capacity)
        else:
            raise ValueError("Cache type must be 'lru', 'lfu', or 'lru_dll'")
        
        self.cache_type = cache_type
        self.ttl = ttl
        self.stats = {
            'queries': 0,
            'cache_hits': 0,
            'cache_misses': 0,
            'database_queries': 0,
            'expired_items': 0,
            'total_query_time': 0.0
        }
    
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> Any:
        """
        Execute database query with caching.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Query result
        """
        start_time = time.time()
        self.stats['queries'] += 1
        
        # Create cache key
        cache_key = self._create_query_key(query, params)
        
        # Try cache first
        cached_result = self.cache.get(cache_key)
        if cached_result and not self._is_expired(cached_result):
            cached_result.update_access()
            self.stats['cache_hits'] += 1
            self.stats['total_query_time'] += time.time() - start_time
            return cached_result.data
        
        # Cache miss or expired
        self.stats['cache_misses'] += 1
        
        # Execute query against database
        result = self._execute_database_query(query, params)
        
        if result is not None:
            self.stats['database_queries'] += 1
            cache_item = CacheItem(
                data=result,
                timestamp=time.time(),
                size=len(str(result))
            )
            self.cache.put(cache_key, cache_item)
        
        self.stats['total_query_time'] += time.time() - start_time
        return result
    
    def _create_query_key(self, query: str, params: Dict[str, Any] = None) -> str:
        """Create a cache key from query and parameters."""
        key_data = query
        if params:
            key_data += json.dumps(params, sort_keys=True)
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def _is_expired(self, cache_item: CacheItem) -> bool:
        """Check if cache item has expired."""
        if time.time() - cache_item.timestamp > self.ttl:
            self.stats['expired_items'] += 1
            return True
        return False
    
    def _execute_database_query(self, query: str, params: Dict[str, Any] = None) -> Any:
        """
        Simulate database query execution.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Simulated query result
        """
        # Simulate database latency (5-20ms)
        time.sleep(random.uniform(0.005, 0.02))
        
        # Simulate different query results
        query_lower = query.lower()
        
        if "select count" in query_lower:
            return {"count": random.randint(1000, 10000)}
        
        elif "select * from users" in query_lower:
            return [
                {"id": 1, "name": "John Doe", "email": "john@example.com"},
                {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
                {"id": 3, "name": "Bob Johnson", "email": "bob@example.com"}
            ]
        
        elif "select * from products" in query_lower:
            return [
                {"id": 1, "name": "Product A", "price": 29.99},
                {"id": 2, "name": "Product B", "price": 49.99},
                {"id": 3, "name": "Product C", "price": 19.99}
            ]
        
        elif "insert" in query_lower:
            return {"affected_rows": 1, "insert_id": random.randint(1000, 9999)}
        
        elif "update" in query_lower:
            return {"affected_rows": random.randint(1, 10)}
        
        elif "delete" in query_lower:
            return {"affected_rows": random.randint(1, 5)}
        
        else:
            return {"result": "Generic query result", "timestamp": time.time()}
    
    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics."""
        avg_query_time = 0.0
        if self.stats['queries'] > 0:
            avg_query_time = self.stats['total_query_time'] / self.stats['queries']
        
        hit_ratio = 0.0
        if self.stats['queries'] > 0:
            hit_ratio = self.stats['cache_hits'] / self.stats['queries']
        
        return {
            **self.stats,
            'hit_ratio': hit_ratio,
            'avg_query_time': avg_query_time,
            'cache_size': len(self.cache),
            'cache_type': self.cache_type,
            'ttl': self.ttl
        }

class CacheComparisonDemo:
    """Demonstration of different cache types in real-world scenarios."""
    
    def __init__(self):
        self.web_caches = {
            'LRU': WebPageCache('lru', capacity=50),
            'LFU': WebPageCache('lfu', capacity=50),
            'LRU_DLL': WebPageCache('lru_dll', capacity=50)
        }
        
        self.db_caches = {
            'LRU': DatabaseQueryCache('lru', capacity=200),
            'LFU': DatabaseQueryCache('lfu', capacity=200),
            'LRU_DLL': DatabaseQueryCache('lru_dll', capacity=200)
        }
    
    def simulate_web_traffic(self, requests: int = 1000) -> Dict[str, Dict[str, Any]]:
        """
        Simulate realistic web traffic patterns.
        
        Args:
            requests: Number of requests to simulate
            
        Returns:
            Dictionary of results for each cache type
        """
        print(f"Simulating {requests} web requests...")
        
        # Define URL patterns with different popularity
        urls = [
            ("/home", 0.4),      # 40% of traffic
            ("/products", 0.3),  # 30% of traffic
            ("/about", 0.1),     # 10% of traffic
            ("/contact", 0.05),  # 5% of traffic
            ("/blog", 0.15)      # 15% of traffic
        ]
        
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15"
        ]
        
        results = {}
        
        for cache_type, cache in self.web_caches.items():
            print(f"  Testing {cache_type} cache...")
            
            # Simulate requests
            for _ in range(requests):
                # Select URL based on popularity
                rand = random.random()
                cumulative = 0
                selected_url = urls[0][0]  # Default
                
                for url, probability in urls:
                    cumulative += probability
                    if rand <= cumulative:
                        selected_url = url
                        break
                
                # Add some variation to URLs
                if "products" in selected_url:
                    selected_url += f"?id={random.randint(1, 100)}"
                elif "blog" in selected_url:
                    selected_url += f"/post-{random.randint(1, 50)}"
                
                # Random user agent
                user_agent = random.choice(user_agents)
                
                # Get page
                cache.get_page(selected_url, user_agent)
            
            results[cache_type] = cache.get_stats()
        
        return results
    
    def simulate_database_workload(self, queries: int = 1000) -> Dict[str, Dict[str, Any]]:
        """
        Simulate realistic database workload.
        
        Args:
            queries: Number of queries to simulate
            
        Returns:
            Dictionary of results for each cache type
        """
        print(f"Simulating {queries} database queries...")
        
        # Define query patterns
        queries_patterns = [
            ("SELECT COUNT(*) FROM users", 0.3),
            ("SELECT * FROM users WHERE id = ?", 0.2),
            ("SELECT * FROM products WHERE category = ?", 0.2),
            ("SELECT * FROM orders WHERE user_id = ?", 0.15),
            ("INSERT INTO logs (message, timestamp) VALUES (?, ?)", 0.1),
            ("UPDATE users SET last_login = ? WHERE id = ?", 0.05)
        ]
        
        results = {}
        
        for cache_type, cache in self.db_caches.items():
            print(f"  Testing {cache_type} cache...")
            
            # Simulate queries
            for _ in range(queries):
                # Select query based on frequency
                rand = random.random()
                cumulative = 0
                selected_query = queries_patterns[0][0]  # Default
                
                for query, probability in queries_patterns:
                    cumulative += probability
                    if rand <= cumulative:
                        selected_query = query
                        break
                
                # Generate parameters
                params = {}
                if "id = ?" in selected_query:
                    params = {"id": random.randint(1, 1000)}
                elif "category = ?" in selected_query:
                    params = {"category": random.choice(["electronics", "clothing", "books"])}
                elif "user_id = ?" in selected_query:
                    params = {"user_id": random.randint(1, 500)}
                elif "INSERT" in selected_query:
                    params = {"message": f"Log entry {random.randint(1, 1000)}", "timestamp": time.time()}
                elif "UPDATE" in selected_query:
                    params = {"last_login": time.time(), "id": random.randint(1, 1000)}
                
                # Execute query
                cache.execute_query(selected_query, params)
            
            results[cache_type] = cache.get_stats()
        
        return results
    
    def run_comprehensive_demo(self):
        """Run comprehensive demonstration of all cache types."""
        print("=" * 80)
        print("REAL-WORLD CACHE APPLICATIONS DEMONSTRATION")
        print("=" * 80)
        print()
        
        # Web cache simulation
        print("WEB CACHE SIMULATION")
        print("-" * 40)
        web_results = self.simulate_web_traffic(1000)
        
        print(f"\n{'Cache Type':<12} {'Hit Ratio':<10} {'Avg Response (ms)':<15} {'Cache Hits':<12} {'Backend Reqs':<12}")
        print("-" * 70)
        
        for cache_type, stats in web_results.items():
            avg_response_ms = stats['avg_response_time'] * 1000
            print(f"{cache_type:<12} {stats['hit_ratio']:<10.3f} {avg_response_ms:<15.2f} "
                  f"{stats['cache_hits']:<12} {stats['backend_requests']:<12}")
        
        print()
        
        # Database cache simulation
        print("DATABASE CACHE SIMULATION")
        print("-" * 40)
        db_results = self.simulate_database_workload(1000)
        
        print(f"\n{'Cache Type':<12} {'Hit Ratio':<10} {'Avg Query (ms)':<15} {'Cache Hits':<12} {'DB Queries':<12}")
        print("-" * 70)
        
        for cache_type, stats in db_results.items():
            avg_query_ms = stats['avg_query_time'] * 1000
            print(f"{cache_type:<12} {stats['hit_ratio']:<10.3f} {avg_query_ms:<15.2f} "
                  f"{stats['cache_hits']:<12} {stats['database_queries']:<12}")
        
        print()
        print("=" * 80)

def main():
    """Main function to run the demonstration."""
    demo = CacheComparisonDemo()
    demo.run_comprehensive_demo()

if __name__ == "__main__":
    main() 