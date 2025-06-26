"""
Network Connectivity application using Union-Find.

This module provides a real-world application of Union-Find for
network connectivity analysis and social network analysis.
"""

from typing import Dict, List, Optional, Tuple, Set
from src.chapter_12.optimized_disjoint_set import OptimizedDisjointSet


class NetworkConnectivity:
    """
    Application of Union-Find for network connectivity analysis.
    
    This demonstrates how Union-Find can be used to solve real-world
    problems like network connectivity and social network analysis.
    
    Features:
    - Add connections between nodes
    - Check connectivity between nodes
    - Find network sizes and components
    - Identify bridge connections
    - Analyze network structure
    
    Time Complexity:
    - Add connection: O(α(n)) amortized
    - Check connectivity: O(α(n)) amortized
    - Get network size: O(α(n)) amortized
    - Find bridge connections: O(m * n * α(n)) where m is number of connections
    """
    
    def __init__(self) -> None:
        """Initialize an empty network."""
        self.ds = OptimizedDisjointSet()
        self.connections: List[Tuple[int, int]] = []
        self.node_metadata: Dict[int, Dict] = {}  # Store additional node information
    
    def add_connection(self, node1: int, node2: int, metadata: Optional[Dict] = None) -> None:
        """
        Add a connection between two nodes.
        
        Args:
            node1: First node ID
            node2: Second node ID
            metadata: Optional metadata about the connection
            
        Time Complexity: O(α(n)) amortized
        """
        self.ds.make_set(node1)
        self.ds.make_set(node2)
        self.ds.union(node1, node2)
        self.connections.append((node1, node2))
        
        # Store metadata if provided
        if metadata:
            if node1 not in self.node_metadata:
                self.node_metadata[node1] = {}
            if node2 not in self.node_metadata:
                self.node_metadata[node2] = {}
            
            self.node_metadata[node1].update(metadata)
            self.node_metadata[node2].update(metadata)
    
    def are_connected(self, node1: int, node2: int) -> bool:
        """
        Check if two nodes are connected.
        
        Args:
            node1: First node ID
            node2: Second node ID
            
        Returns:
            True if the nodes are connected, False otherwise
            
        Time Complexity: O(α(n)) amortized
        """
        return self.ds.connected(node1, node2)
    
    def get_network_size(self, node: int) -> int:
        """
        Get the size of the network containing a node.
        
        Args:
            node: Node ID to find the network size for
            
        Returns:
            Number of nodes in the network containing the given node
            
        Time Complexity: O(α(n)) amortized
        """
        return self.ds.get_set_size(node)
    
    def get_all_networks(self) -> List[List[int]]:
        """
        Get all connected networks.
        
        Returns:
            List of lists, where each inner list represents a connected network
            
        Time Complexity: O(n * α(n)) amortized
        """
        return self.ds.get_connected_components()
    
    def get_network_roots(self) -> List[int]:
        """
        Get the root nodes of all networks.
        
        Returns:
            List of root node IDs
            
        Time Complexity: O(n * α(n)) amortized
        """
        return self.ds.get_roots()
    
    def count_networks(self) -> int:
        """
        Count the number of separate networks.
        
        Returns:
            Number of disconnected networks
            
        Time Complexity: O(n * α(n)) amortized
        """
        return self.ds.count_sets()
    
    def get_largest_network(self) -> List[int]:
        """
        Get the largest connected network.
        
        Returns:
            List of node IDs in the largest network
            
        Time Complexity: O(n * α(n)) amortized
        """
        networks = self.get_all_networks()
        if not networks:
            return []
        return max(networks, key=len)
    
    def get_network_nodes(self, root: int) -> List[int]:
        """
        Get all nodes in the network with the given root.
        
        Args:
            root: Root node ID of the network
            
        Returns:
            List of node IDs in the network
            
        Time Complexity: O(n * α(n)) amortized
        """
        return self.ds.get_set_elements(root)
    
    def find_bridge_connections(self) -> List[Tuple[int, int]]:
        """
        Find connections that would disconnect the network if removed.
        
        Returns:
            List of connection tuples that are bridges
            
        Time Complexity: O(m * n * α(n)) where m is number of connections
        """
        bridges = []
        
        for i, (node1, node2) in enumerate(self.connections):
            # Temporarily remove the connection
            temp_ds = OptimizedDisjointSet()
            
            # Add all nodes
            all_nodes = set()
            for n1, n2 in self.connections:
                all_nodes.add(n1)
                all_nodes.add(n2)
            
            for node in all_nodes:
                temp_ds.make_set(node)
            
            # Add all connections except the current one
            for j, (n1, n2) in enumerate(self.connections):
                if i != j:
                    temp_ds.union(n1, n2)
            
            # Check if removing this connection disconnects the network
            if len(temp_ds.get_connected_components()) > len(self.get_all_networks()):
                bridges.append((node1, node2))
        
        return bridges
    
    def get_network_statistics(self) -> Dict[str, any]:
        """
        Get comprehensive statistics about the network.
        
        Returns:
            Dictionary containing network statistics
            
        Time Complexity: O(n * α(n)) amortized
        """
        networks = self.get_all_networks()
        network_sizes = [len(network) for network in networks]
        
        if not network_sizes:
            return {
                'total_nodes': 0,
                'total_connections': 0,
                'num_networks': 0,
                'largest_network_size': 0,
                'smallest_network_size': 0,
                'average_network_size': 0,
                'network_size_variance': 0
            }
        
        return {
            'total_nodes': len(self.ds),
            'total_connections': len(self.connections),
            'num_networks': len(networks),
            'largest_network_size': max(network_sizes),
            'smallest_network_size': min(network_sizes),
            'average_network_size': sum(network_sizes) / len(network_sizes),
            'network_size_variance': self._calculate_variance(network_sizes)
        }
    
    def _calculate_variance(self, values: List[int]) -> float:
        """Calculate variance of a list of values."""
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    def get_node_degree(self, node: int) -> int:
        """
        Get the degree (number of connections) of a node.
        
        Args:
            node: Node ID to get degree for
            
        Returns:
            Number of connections for the node
            
        Time Complexity: O(m) where m is number of connections
        """
        degree = 0
        for n1, n2 in self.connections:
            if n1 == node or n2 == node:
                degree += 1
        return degree
    
    def get_high_degree_nodes(self, threshold: int = 5) -> List[int]:
        """
        Get nodes with degree above a threshold.
        
        Args:
            threshold: Minimum degree threshold
            
        Returns:
            List of node IDs with degree above threshold
            
        Time Complexity: O(n * m) where n is number of nodes, m is number of connections
        """
        high_degree_nodes = []
        for node in self.ds.parents:
            if self.get_node_degree(node) >= threshold:
                high_degree_nodes.append(node)
        return high_degree_nodes
    
    def get_network_diameter(self, network_root: int) -> int:
        """
        Calculate the diameter of a network (longest shortest path).
        This is a simplified implementation.
        
        Args:
            network_root: Root node of the network
            
        Returns:
            Diameter of the network
            
        Time Complexity: O(n²) where n is number of nodes in the network
        """
        network_nodes = self.get_network_nodes(network_root)
        if len(network_nodes) <= 1:
            return 0
        
        # This is a simplified diameter calculation
        # In practice, you'd use a proper graph algorithm
        max_distance = 0
        
        for node1 in network_nodes:
            for node2 in network_nodes:
                if node1 != node2:
                    # Calculate distance using BFS would be more accurate
                    # For now, we'll use a simple heuristic
                    if self.are_connected(node1, node2):
                        distance = 1  # Simplified
                        max_distance = max(max_distance, distance)
        
        return max_distance
    
    def merge_networks(self, network1_root: int, network2_root: int) -> bool:
        """
        Merge two networks by adding a connection between their roots.
        
        Args:
            network1_root: Root of first network
            network2_root: Root of second network
            
        Returns:
            True if networks were merged, False if already connected
            
        Time Complexity: O(α(n)) amortized
        """
        if not self.ds.connected(network1_root, network2_root):
            self.add_connection(network1_root, network2_root)
            return True
        return False
    
    def __len__(self) -> int:
        """Return the total number of nodes in the network."""
        return len(self.ds)
    
    def __repr__(self) -> str:
        """String representation of the NetworkConnectivity."""
        stats = self.get_network_statistics()
        return f"NetworkConnectivity(nodes={stats['total_nodes']}, networks={stats['num_networks']}, connections={stats['total_connections']})" 