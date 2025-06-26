"""
Image Segmentation application using Union-Find.

This module provides a real-world application of Union-Find for
computer vision tasks like connected component labeling and image segmentation.
"""

from typing import Dict, List, Optional, Tuple, Set
from src.chapter_12.optimized_disjoint_set import OptimizedDisjointSet


class ImageSegmentation:
    """
    Application of Union-Find for image segmentation.
    
    This demonstrates how Union-Find can be used in computer vision
    for connected component labeling and image segmentation.
    
    Features:
    - Set pixel values and automatically update connected components
    - Get image segments and their properties
    - Analyze segment sizes and distributions
    - Support for different connectivity patterns
    
    Time Complexity:
    - Set pixel: O(1) amortized
    - Get segments: O(n * α(n)) amortized where n is number of pixels
    - Get segment size: O(α(n)) amortized
    """
    
    def __init__(self, width: int, height: int) -> None:
        """
        Initialize an image segmentation system.
        
        Args:
            width: Width of the image in pixels
            height: Height of the image in pixels
        """
        self.width = width
        self.height = height
        self.ds = OptimizedDisjointSet()
        self.pixels = [[0 for _ in range(width)] for _ in range(height)]
        
        # Initialize all pixels as separate sets
        for y in range(height):
            for x in range(width):
                pixel_id = y * width + x
                self.ds.make_set(pixel_id)
    
    def set_pixel(self, x: int, y: int, value: int) -> None:
        """
        Set a pixel value and update connected components.
        
        Args:
            x: X coordinate of the pixel
            y: Y coordinate of the pixel
            value: Pixel value (0 for background, >0 for foreground)
            
        Raises:
            ValueError: If coordinates are out of bounds
            
        Time Complexity: O(1) amortized
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError("Pixel coordinates out of bounds")
        
        self.pixels[y][x] = value
        pixel_id = y * self.width + x
        
        # Union with neighboring pixels of the same value
        neighbors = self._get_neighbors(x, y)
        for nx, ny in neighbors:
            if (0 <= nx < self.width and 0 <= ny < self.height and 
                self.pixels[ny][nx] == value):
                neighbor_id = ny * self.width + nx
                self.ds.union(pixel_id, neighbor_id)
    
    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get 4-connected neighbors of a pixel.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of (x, y) coordinates of neighboring pixels
        """
        return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    
    def _get_8_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get 8-connected neighbors of a pixel.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            List of (x, y) coordinates of neighboring pixels
        """
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    neighbors.append((x + dx, y + dy))
        return neighbors
    
    def get_segments(self) -> Dict[int, List[Tuple[int, int]]]:
        """
        Get all image segments as lists of pixel coordinates.
        
        Returns:
            Dictionary mapping segment root to list of (x, y) coordinates
            
        Time Complexity: O(n * α(n)) amortized where n is number of pixels
        """
        segments = {}
        
        for y in range(self.height):
            for x in range(self.width):
                if self.pixels[y][x] != 0:  # Non-background pixel
                    pixel_id = y * self.width + x
                    root = self.ds.find(pixel_id)
                    
                    if root not in segments:
                        segments[root] = []
                    segments[root].append((x, y))
        
        return segments
    
    def get_segment_size(self, x: int, y: int) -> int:
        """
        Get the size of the segment containing pixel (x, y).
        
        Args:
            x: X coordinate of the pixel
            y: Y coordinate of the pixel
            
        Returns:
            Number of pixels in the segment
            
        Time Complexity: O(α(n)) amortized
        """
        pixel_id = y * self.width + x
        return self.ds.get_set_size(pixel_id)
    
    def count_segments(self) -> int:
        """
        Count the number of distinct segments in the image.
        
        Returns:
            Number of segments
            
        Time Complexity: O(n * α(n)) amortized
        """
        return len(self.get_segments())
    
    def get_segment_statistics(self) -> Dict[str, any]:
        """
        Get comprehensive statistics about image segments.
        
        Returns:
            Dictionary containing segment statistics
            
        Time Complexity: O(n * α(n)) amortized
        """
        segments = self.get_segments()
        segment_sizes = [len(segment) for segment in segments.values()]
        
        if not segment_sizes:
            return {
                'num_segments': 0,
                'total_foreground_pixels': 0,
                'largest_segment_size': 0,
                'smallest_segment_size': 0,
                'average_segment_size': 0,
                'segment_size_variance': 0
            }
        
        return {
            'num_segments': len(segments),
            'total_foreground_pixels': sum(segment_sizes),
            'largest_segment_size': max(segment_sizes),
            'smallest_segment_size': min(segment_sizes),
            'average_segment_size': sum(segment_sizes) / len(segment_sizes),
            'segment_size_variance': self._calculate_variance(segment_sizes)
        }
    
    def _calculate_variance(self, values: List[int]) -> float:
        """Calculate variance of a list of values."""
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    def get_segment_centroid(self, segment_pixels: List[Tuple[int, int]]) -> Tuple[float, float]:
        """
        Calculate the centroid of a segment.
        
        Args:
            segment_pixels: List of (x, y) coordinates in the segment
            
        Returns:
            (x, y) coordinates of the centroid
            
        Time Complexity: O(k) where k is number of pixels in segment
        """
        if not segment_pixels:
            return (0.0, 0.0)
        
        sum_x = sum(x for x, y in segment_pixels)
        sum_y = sum(y for x, y in segment_pixels)
        
        return (sum_x / len(segment_pixels), sum_y / len(segment_pixels))
    
    def get_segment_bounds(self, segment_pixels: List[Tuple[int, int]]) -> Tuple[int, int, int, int]:
        """
        Get the bounding box of a segment.
        
        Args:
            segment_pixels: List of (x, y) coordinates in the segment
            
        Returns:
            (min_x, min_y, max_x, max_y) bounding box coordinates
            
        Time Complexity: O(k) where k is number of pixels in segment
        """
        if not segment_pixels:
            return (0, 0, 0, 0)
        
        min_x = min(x for x, y in segment_pixels)
        max_x = max(x for x, y in segment_pixels)
        min_y = min(y for x, y in segment_pixels)
        max_y = max(y for x, y in segment_pixels)
        
        return (min_x, min_y, max_x, max_y)
    
    def get_large_segments(self, min_size: int = 10) -> Dict[int, List[Tuple[int, int]]]:
        """
        Get segments larger than a minimum size.
        
        Args:
            min_size: Minimum segment size threshold
            
        Returns:
            Dictionary of large segments
            
        Time Complexity: O(n * α(n)) amortized
        """
        segments = self.get_segments()
        return {root: pixels for root, pixels in segments.items() if len(pixels) >= min_size}
    
    def get_segment_by_size(self, target_size: int) -> List[List[Tuple[int, int]]]:
        """
        Get all segments of a specific size.
        
        Args:
            target_size: Target segment size
            
        Returns:
            List of segments with the target size
            
        Time Complexity: O(n * α(n)) amortized
        """
        segments = self.get_segments()
        return [pixels for pixels in segments.values() if len(pixels) == target_size]
    
    def merge_segments(self, segment1_root: int, segment2_root: int) -> bool:
        """
        Merge two segments by connecting their pixels.
        
        Args:
            segment1_root: Root of first segment
            segment2_root: Root of second segment
            
        Returns:
            True if segments were merged, False if already connected
            
        Time Complexity: O(α(n)) amortized
        """
        if not self.ds.connected(segment1_root, segment2_root):
            self.ds.union(segment1_root, segment2_root)
            return True
        return False
    
    def get_segment_connectivity(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Get all pixels connected to a given pixel.
        
        Args:
            x: X coordinate of the pixel
            y: Y coordinate of the pixel
            
        Returns:
            List of (x, y) coordinates of connected pixels
            
        Time Complexity: O(n * α(n)) amortized
        """
        pixel_id = y * self.width + x
        root = self.ds.find(pixel_id)
        
        connected_pixels = []
        for py in range(self.height):
            for px in range(self.width):
                if self.pixels[py][px] != 0:  # Non-background pixel
                    neighbor_id = py * self.width + px
                    if self.ds.connected(pixel_id, neighbor_id):
                        connected_pixels.append((px, py))
        
        return connected_pixels
    
    def clear_image(self) -> None:
        """Clear the image and reset all segments."""
        self.pixels = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.ds = OptimizedDisjointSet()
        
        # Reinitialize all pixels as separate sets
        for y in range(self.height):
            for x in range(self.width):
                pixel_id = y * self.width + x
                self.ds.make_set(pixel_id)
    
    def get_image_array(self) -> List[List[int]]:
        """
        Get the current image as a 2D array.
        
        Returns:
            2D array representing the image
        """
        return [row[:] for row in self.pixels]
    
    def set_image_array(self, image_array: List[List[int]]) -> None:
        """
        Set the image from a 2D array and update segments.
        
        Args:
            image_array: 2D array representing the image
            
        Raises:
            ValueError: If array dimensions don't match
        """
        if (len(image_array) != self.height or 
            any(len(row) != self.width for row in image_array)):
            raise ValueError("Image array dimensions don't match")
        
        # Clear current image
        self.clear_image()
        
        # Set pixels and update segments
        for y in range(self.height):
            for x in range(self.width):
                self.set_pixel(x, y, image_array[y][x])
    
    def __len__(self) -> Tuple[int, int]:
        """Return the dimensions of the image."""
        return (self.width, self.height)
    
    def __repr__(self) -> str:
        """String representation of the ImageSegmentation."""
        stats = self.get_segment_statistics()
        return f"ImageSegmentation({self.width}x{self.height}, segments={stats['num_segments']})" 