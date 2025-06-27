"""
Undo/Redo system implementation using linked lists.

This module demonstrates a practical application of linked lists in the form
of an undo/redo system that maintains a history of actions.
"""

import time
from typing import TypeVar, Generic, Optional, Any, Callable, Dict, List
from dataclasses import dataclass
from .doubly_linked_list import DoublyLinkedList

T = TypeVar('T')

@dataclass
class Action(Generic[T]):
    """
    Represents an action in the undo/redo system.
    
    This class encapsulates an action with its execution and undo functions,
    along with metadata like name, timestamp, and description.
    
    Attributes:
        name: Human-readable name of the action
        do_action: Function to execute the action
        undo_action: Function to undo the action
        timestamp: When the action was created
        description: Optional description of the action
    """
    name: str
    do_action: Callable[[], T]
    undo_action: Callable[[T], None]
    timestamp: float
    description: str = ""
    result: T = None

class UndoRedoSystem(Generic[T]):
    """
    An undo/redo system implemented using linked lists.
    
    This system maintains a history of actions that can be undone and redone.
    It uses a doubly linked list to efficiently navigate through the action history.
    
    Attributes:
        _history: Doubly linked list storing action history
        _current_position: Current position in the history (-1 means before first action)
        _max_history: Maximum number of actions to keep in history
        _is_executing: Flag to prevent recursive execution
    """
    
    def __init__(self, max_history: int = 100) -> None:
        """
        Initialize the undo/redo system.
        
        Args:
            max_history: Maximum number of actions to keep in history
        """
        if max_history <= 0:
            raise ValueError("max_history must be positive")
        
        self._history = DoublyLinkedList[Action[T]]()
        self._current_position = -1  # -1 means before first action
        self._max_history = max_history
        self._is_executing = False  # Prevent recursive execution
    
    def execute_action(self, name: str, do_action: Callable[[], T], 
                      undo_action: Callable[[T], None], 
                      description: str = "") -> T:
        """
        Execute an action and add it to the history.
        
        Args:
            name: Name of the action
            do_action: Function to execute the action
            undo_action: Function to undo the action
            description: Optional description of the action
            
        Returns:
            The result of executing the action
            
        Raises:
            RuntimeError: If another action is currently being executed
        """
        if self._is_executing:
            raise RuntimeError("Cannot execute action while another action is being executed")
        
        self._is_executing = True
        
        try:
            # Execute the action
            result = do_action()
            
            # Create action record with the result
            action = Action(
                name=name,
                do_action=do_action,
                undo_action=undo_action,
                timestamp=time.time(),
                description=description
            )
            # Store the result for undo
            action.result = result
            
            # Clear any redo history
            self._clear_redo_history()
            
            # Add to history
            self._history.append(action)
            self._current_position += 1
            
            # Maintain max history size
            if len(self._history) > self._max_history:
                self._history._head_sentinel.next = self._history._head_sentinel.next.next
                self._history._head_sentinel.next.prev = self._history._head_sentinel
                self._history._size -= 1
                self._current_position -= 1
            
            return result
            
        finally:
            self._is_executing = False
    
    def can_undo(self) -> bool:
        """
        Check if undo is possible.
        
        Returns:
            True if there are actions that can be undone
        """
        return self._current_position >= 0
    
    def can_redo(self) -> bool:
        """
        Check if redo is possible.
        
        Returns:
            True if there are actions that can be redone
        """
        return self._current_position < len(self._history) - 1
    
    def undo(self) -> Optional[str]:
        """
        Undo the last action.
        
        Returns:
            Name of the undone action, or None if no action to undo
            
        Raises:
            RuntimeError: If another action is currently being executed
        """
        if not self.can_undo():
            return None
        
        if self._is_executing:
            raise RuntimeError("Cannot undo while an action is being executed")
        
        self._is_executing = True
        
        try:
            # Get the action to undo
            action = self._history.get_at_index(self._current_position)
            
            # Execute undo with the stored result
            action.undo_action(action.result)
            
            # Move position back
            self._current_position -= 1
            
            return action.name
            
        finally:
            self._is_executing = False
    
    def redo(self) -> Optional[str]:
        """
        Redo the next action.
        
        Returns:
            Name of the redone action, or None if no action to redo
            
        Raises:
            RuntimeError: If another action is currently being executed
        """
        if not self.can_redo():
            return None
        
        if self._is_executing:
            raise RuntimeError("Cannot redo while an action is being executed")
        
        self._is_executing = True
        
        try:
            # Move position forward
            self._current_position += 1
            
            # Get the action to redo
            action = self._history.get_at_index(self._current_position)
            
            # Execute the action
            action.do_action()
            
            return action.name
            
        finally:
            self._is_executing = False
    
    def _clear_redo_history(self) -> None:
        """Clear any redo history when a new action is executed."""
        while self._current_position < len(self._history) - 1:
            # Remove from end
            self._history._tail_sentinel.prev = self._history._tail_sentinel.prev.prev
            self._history._tail_sentinel.prev.next = self._history._tail_sentinel
            self._history._size -= 1
    
    def get_history_info(self) -> Dict[str, Any]:
        """
        Get information about the current history state.
        
        Returns:
            Dictionary containing history statistics
        """
        return {
            "total_actions": len(self._history),
            "current_position": self._current_position,
            "can_undo": self.can_undo(),
            "can_redo": self.can_redo(),
            "max_history": self._max_history
        }
    
    def clear_history(self) -> None:
        """Clear all history."""
        self._history = DoublyLinkedList[Action[T]]()
        self._current_position = -1
    
    def get_action_names(self) -> List[str]:
        """
        Get a list of all action names in order.
        
        Returns:
            List of action names in chronological order
        """
        return [action.name for action in self._history]
    
    def get_action_descriptions(self) -> List[str]:
        """
        Get a list of all action descriptions in order.
        
        Returns:
            List of action descriptions in chronological order
        """
        return [action.description for action in self._history]
    
    def get_action_timestamps(self) -> List[float]:
        """
        Get a list of all action timestamps in order.
        
        Returns:
            List of action timestamps in chronological order
        """
        return [action.timestamp for action in self._history]
    
    def get_current_action(self) -> Optional[Action[T]]:
        """
        Get the current action (the one that would be undone next).
        
        Returns:
            The current action, or None if no actions exist
        """
        if not self.can_undo():
            return None
        return self._history.get_at_index(self._current_position)
    
    def get_next_action(self) -> Optional[Action[T]]:
        """
        Get the next action (the one that would be redone next).
        
        Returns:
            The next action, or None if no actions can be redone
        """
        if not self.can_redo():
            return None
        return self._history.get_at_index(self._current_position + 1)
    
    def undo_multiple(self, count: int) -> List[str]:
        """
        Undo multiple actions at once.
        
        Args:
            count: Number of actions to undo
            
        Returns:
            List of names of undone actions
            
        Raises:
            ValueError: If count is negative
            RuntimeError: If another action is currently being executed
        """
        if count < 0:
            raise ValueError("Count must be non-negative")
        
        if self._is_executing:
            raise RuntimeError("Cannot undo while an action is being executed")
        
        undone_actions = []
        available_undo = self._current_position + 1  # +1 because position 0 means 1 action can be undone
        
        # Undo up to the available count or requested count, whichever is smaller
        actual_count = min(count, available_undo)
        
        for _ in range(actual_count):
            action_name = self.undo()
            if action_name:
                undone_actions.append(action_name)
        
        return undone_actions
    
    def redo_multiple(self, count: int) -> List[str]:
        """
        Redo multiple actions at once.
        
        Args:
            count: Number of actions to redo
            
        Returns:
            List of names of redone actions
            
        Raises:
            ValueError: If count is negative
            RuntimeError: If another action is currently being executed
        """
        if count < 0:
            raise ValueError("Count must be non-negative")
        
        if self._is_executing:
            raise RuntimeError("Cannot redo while an action is being executed")
        
        redone_actions = []
        available_redo = len(self._history) - 1 - self._current_position
        
        # Redo up to the available count or requested count, whichever is smaller
        actual_count = min(count, available_redo)
        
        for _ in range(actual_count):
            action_name = self.redo()
            if action_name:
                redone_actions.append(action_name)
        
        return redone_actions
    
    def get_history_size(self) -> int:
        """
        Get the current size of the history.
        
        Returns:
            Number of actions in the history
        """
        return len(self._history)
    
    def is_empty(self) -> bool:
        """
        Check if the history is empty.
        
        Returns:
            True if no actions have been executed
        """
        return len(self._history) == 0
    
    def set_max_history(self, max_history: int) -> None:
        """
        Set the maximum history size.
        
        Args:
            max_history: New maximum number of actions to keep
            
        Raises:
            ValueError: If max_history is not positive
        """
        if max_history <= 0:
            raise ValueError("max_history must be positive")
        
        self._max_history = max_history
        
        # Trim history if necessary
        while len(self._history) > self._max_history:
            self._history._head_sentinel.next = self._history._head_sentinel.next.next
            self._history._head_sentinel.next.prev = self._history._head_sentinel
            self._history._size -= 1
            self._current_position = max(-1, self._current_position - 1) 



def main():
    """Main function to demonstrate the module functionality."""
    print(f"Running undo_redo demonstration...")
    print("=" * 50)

    # Create instance of Action
    try:
        instance = Action()
        print(f"✓ Created Action instance successfully")
        print(f"  Instance: {instance}")

        # Demonstrate basic functionality
        print("Testing basic functionality...")
        print(f"  Instance type: {type(instance)}")
    except Exception as e:
        print(f"✗ Error creating Action instance: {e}")
        return False

    # Module status
    print("✓ Module loaded successfully!")
    print("✓ Ready for interactive use in Pyodide.")

    return True

if __name__ == "__main__":
    main()
