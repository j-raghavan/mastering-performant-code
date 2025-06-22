"""
Unit tests for UndoRedoSystem implementation.

This module provides comprehensive tests for the UndoRedoSystem class,
ensuring 100% code coverage and testing all edge cases.
"""

import pytest
import time
from typing import List

from src.chapter_04.undo_redo import UndoRedoSystem, Action


class TestUndoRedoSystem:
    """Test cases for UndoRedoSystem class."""
    
    def test_init_default(self):
        """Test initialization with default parameters."""
        system = UndoRedoSystem()
        assert system._max_history == 100
        assert system._current_position == -1
        assert len(system._history) == 0
        assert not system._is_executing
    
    def test_init_custom_max_history(self):
        """Test initialization with custom max history."""
        system = UndoRedoSystem(max_history=50)
        assert system._max_history == 50
        assert system._current_position == -1
        assert len(system._history) == 0
    
    def test_init_invalid_max_history(self):
        """Test initialization with invalid max history."""
        with pytest.raises(ValueError, match="max_history must be positive"):
            UndoRedoSystem(max_history=0)
        
        with pytest.raises(ValueError, match="max_history must be positive"):
            UndoRedoSystem(max_history=-1)
    
    def test_execute_action_success(self):
        """Test successful action execution."""
        system = UndoRedoSystem()
        
        def do_action():
            return "result"
        
        def undo_action(result):
            pass
        
        result = system.execute_action("test_action", do_action, undo_action, "test description")
        
        assert result == "result"
        assert len(system._history) == 1
        assert system._current_position == 0
        assert system._history.get_at_index(0).name == "test_action"
        assert system._history.get_at_index(0).description == "test description"
    
    def test_execute_action_recursive_error(self):
        """Test action execution during another action."""
        system = UndoRedoSystem()
        
        def do_action():
            # Try to execute another action while this one is running
            system.execute_action("nested", lambda: None, lambda x: None)
            return "result"
        
        def undo_action(result):
            pass
        
        with pytest.raises(RuntimeError, match="Cannot execute action while another action is being executed"):
            system.execute_action("test_action", do_action, undo_action)
    
    def test_can_undo_empty(self):
        """Test can_undo on empty system."""
        system = UndoRedoSystem()
        assert system.can_undo() is False
    
    def test_can_undo_with_actions(self):
        """Test can_undo with actions."""
        system = UndoRedoSystem()
        
        system.execute_action("action1", lambda: None, lambda x: None)
        assert system.can_undo() is True
        
        system.undo()
        assert system.can_undo() is False
    
    def test_can_redo_empty(self):
        """Test can_redo on empty system."""
        system = UndoRedoSystem()
        assert system.can_redo() is False
    
    def test_can_redo_with_actions(self):
        """Test can_redo with actions."""
        system = UndoRedoSystem()
        
        system.execute_action("action1", lambda: None, lambda x: None)
        assert system.can_redo() is False
        
        system.undo()
        assert system.can_redo() is True
    
    def test_undo_success(self):
        """Test successful undo operation."""
        system = UndoRedoSystem()
        
        # Simulate a simple counter
        counter = 0
        
        def increment():
            nonlocal counter
            counter += 1
            return counter - 1
        
        def decrement(old_value):
            nonlocal counter
            counter = old_value
        
        system.execute_action("increment", increment, decrement)
        assert counter == 1
        
        action_name = system.undo()
        assert action_name == "increment"
        assert counter == 0
        assert system._current_position == -1
    
    def test_undo_empty(self):
        """Test undo on empty system."""
        system = UndoRedoSystem()
        result = system.undo()
        assert result is None
    
    def test_undo_during_execution(self):
        """Test undo during action execution."""
        system = UndoRedoSystem()
        
        # First execute an action
        system.execute_action("test", lambda: None, lambda x: None)
        
        # Now try to call undo from within an action execution
        def do_action():
            system.undo()
            return None
        
        def undo_action(result):
            pass
        
        # This should raise an error because we're trying to undo during execution
        with pytest.raises(RuntimeError, match="Cannot undo while an action is being executed"):
            system.execute_action("test2", do_action, undo_action)
    
    def test_redo_success(self):
        """Test successful redo operation."""
        system = UndoRedoSystem()
        
        # Simulate a simple counter
        counter = 0
        
        def increment():
            nonlocal counter
            counter += 1
            return counter - 1
        
        def decrement(old_value):
            nonlocal counter
            counter = old_value
        
        system.execute_action("increment", increment, decrement)
        assert counter == 1
        
        system.undo()
        assert counter == 0
        
        action_name = system.redo()
        assert action_name == "increment"
        assert counter == 1
        assert system._current_position == 0
    
    def test_redo_empty(self):
        """Test redo on empty system."""
        system = UndoRedoSystem()
        result = system.redo()
        assert result is None
    
    def test_redo_during_execution(self):
        """Test redo during action execution."""
        system = UndoRedoSystem()
        
        # First execute an action and undo it
        system.execute_action("test", lambda: None, lambda x: None)
        system.undo()
        
        # Now try to call redo from within an action execution
        def do_action():
            system.redo()
            return None
        
        def undo_action(result):
            pass
        
        # This should raise an error because we're trying to redo during execution
        with pytest.raises(RuntimeError, match="Cannot redo while an action is being executed"):
            system.execute_action("test2", do_action, undo_action)
    
    def test_clear_redo_history(self):
        """Test clearing redo history when new action is executed."""
        system = UndoRedoSystem()
        
        # Execute some actions
        system.execute_action("action1", lambda: None, lambda x: None)
        system.execute_action("action2", lambda: None, lambda x: None)
        system.execute_action("action3", lambda: None, lambda x: None)
        
        # Undo some actions
        system.undo()
        system.undo()
        
        # Should be able to redo
        assert system.can_redo() is True
        
        # Execute new action - should clear redo history
        system.execute_action("action4", lambda: None, lambda x: None)
        
        # Should not be able to redo anymore
        assert system.can_redo() is False
    
    def test_get_history_info(self):
        """Test get_history_info method."""
        system = UndoRedoSystem(max_history=50)
        
        # Empty system
        info = system.get_history_info()
        assert info["total_actions"] == 0
        assert info["current_position"] == -1
        assert info["can_undo"] is False
        assert info["can_redo"] is False
        assert info["max_history"] == 50
        
        # With actions
        system.execute_action("action1", lambda: None, lambda x: None)
        system.execute_action("action2", lambda: None, lambda x: None)
        
        info = system.get_history_info()
        assert info["total_actions"] == 2
        assert info["current_position"] == 1
        assert info["can_undo"] is True
        assert info["can_redo"] is False
    
    def test_clear_history(self):
        """Test clear_history method."""
        system = UndoRedoSystem()
        
        # Add some actions
        system.execute_action("action1", lambda: None, lambda x: None)
        system.execute_action("action2", lambda: None, lambda x: None)
        
        assert len(system._history) == 2
        assert system._current_position == 1
        
        # Clear history
        system.clear_history()
        
        assert len(system._history) == 0
        assert system._current_position == -1
        assert not system.can_undo()
        assert not system.can_redo()
    
    def test_get_action_names(self):
        """Test get_action_names method."""
        system = UndoRedoSystem()
        
        # Empty system
        names = system.get_action_names()
        assert names == []
        
        # With actions
        system.execute_action("action1", lambda: None, lambda x: None)
        system.execute_action("action2", lambda: None, lambda x: None)
        system.execute_action("action3", lambda: None, lambda x: None)
        
        names = system.get_action_names()
        assert names == ["action1", "action2", "action3"]
    
    def test_get_action_descriptions(self):
        """Test get_action_descriptions method."""
        system = UndoRedoSystem()
        
        # Empty system
        descriptions = system.get_action_descriptions()
        assert descriptions == []
        
        # With actions
        system.execute_action("action1", lambda: None, lambda x: None, "desc1")
        system.execute_action("action2", lambda: None, lambda x: None, "desc2")
        
        descriptions = system.get_action_descriptions()
        assert descriptions == ["desc1", "desc2"]
    
    def test_get_action_timestamps(self):
        """Test get_action_timestamps method."""
        system = UndoRedoSystem()
        
        # Empty system
        timestamps = system.get_action_timestamps()
        assert timestamps == []
        
        # With actions
        system.execute_action("action1", lambda: None, lambda x: None)
        system.execute_action("action2", lambda: None, lambda x: None)
        
        timestamps = system.get_action_timestamps()
        assert len(timestamps) == 2
        assert all(isinstance(ts, float) for ts in timestamps)
        assert timestamps[0] <= timestamps[1]  # Should be in chronological order
    
    def test_get_current_action(self):
        """Test get_current_action method."""
        system = UndoRedoSystem()
        
        # Empty system
        action = system.get_current_action()
        assert action is None
        
        # With actions
        system.execute_action("action1", lambda: None, lambda x: None)
        action = system.get_current_action()
        assert action is not None
        assert action.name == "action1"
    
    def test_get_next_action(self):
        """Test get_next_action method."""
        system = UndoRedoSystem()
        
        # Empty system
        action = system.get_next_action()
        assert action is None
        
        # With actions but no redo available
        system.execute_action("action1", lambda: None, lambda x: None)
        action = system.get_next_action()
        assert action is None
        
        # With redo available
        system.undo()
        action = system.get_next_action()
        assert action is not None
        assert action.name == "action1"
    
    def test_undo_multiple_success(self):
        """Test undo_multiple method."""
        system = UndoRedoSystem()
        
        # Add actions
        for i in range(5):
            system.execute_action(f"action{i}", lambda: None, lambda x: None)
        
        # Undo multiple actions
        undone = system.undo_multiple(3)
        assert len(undone) == 3
        assert undone == ["action4", "action3", "action2"]
        assert system._current_position == 1
    
    def test_undo_multiple_partial(self):
        """Test undo_multiple with more actions than available."""
        system = UndoRedoSystem()
        
        # Add actions
        for i in range(3):
            system.execute_action(f"action{i}", lambda: None, lambda x: None)
        
        # Try to undo more than available
        undone = system.undo_multiple(5)
        assert len(undone) == 3
        assert undone == ["action2", "action1", "action0"]
        assert system._current_position == -1
    
    def test_undo_multiple_invalid_count(self):
        """Test undo_multiple with invalid count."""
        system = UndoRedoSystem()
        system.execute_action("action1", lambda: None, lambda x: None)
        
        with pytest.raises(ValueError, match="Count must be non-negative"):
            system.undo_multiple(-1)
    
    def test_redo_multiple_success(self):
        """Test redo_multiple method."""
        system = UndoRedoSystem()
        
        # Add actions and undo them
        for i in range(5):
            system.execute_action(f"action{i}", lambda: None, lambda x: None)
        
        system.undo_multiple(3)
        
        # Redo multiple actions
        redone = system.redo_multiple(2)
        assert len(redone) == 2
        assert redone == ["action2", "action3"]
        assert system._current_position == 3
    
    def test_redo_multiple_partial(self):
        """Test redo_multiple with more actions than available."""
        system = UndoRedoSystem()
        
        # Add actions and undo them
        for i in range(3):
            system.execute_action(f"action{i}", lambda: None, lambda x: None)
        
        system.undo_multiple(2)
        
        # Try to redo more than available
        redone = system.redo_multiple(5)
        assert len(redone) == 2
        assert redone == ["action1", "action2"]
        assert system._current_position == 2
    
    def test_redo_multiple_invalid_count(self):
        """Test redo_multiple with invalid count."""
        system = UndoRedoSystem()
        system.execute_action("action1", lambda: None, lambda x: None)
        system.undo()
        
        with pytest.raises(ValueError, match="Count must be non-negative"):
            system.redo_multiple(-1)
    
    def test_get_history_size(self):
        """Test get_history_size method."""
        system = UndoRedoSystem()
        
        # Empty system
        assert system.get_history_size() == 0
        
        # With actions
        system.execute_action("action1", lambda: None, lambda x: None)
        system.execute_action("action2", lambda: None, lambda x: None)
        
        assert system.get_history_size() == 2
    
    def test_is_empty(self):
        """Test is_empty method."""
        system = UndoRedoSystem()
        
        # Empty system
        assert system.is_empty() is True
        
        # With actions
        system.execute_action("action1", lambda: None, lambda x: None)
        assert system.is_empty() is False
    
    def test_set_max_history_valid(self):
        """Test set_max_history with valid value."""
        system = UndoRedoSystem(max_history=10)
        
        # Add some actions
        for i in range(5):
            system.execute_action(f"action{i}", lambda: None, lambda x: None)
        
        # Set new max history
        system.set_max_history(3)
        assert system._max_history == 3
        assert len(system._history) == 3  # Should be trimmed
        assert system._current_position == 2
    
    def test_set_max_history_invalid(self):
        """Test set_max_history with invalid value."""
        system = UndoRedoSystem()
        
        with pytest.raises(ValueError, match="max_history must be positive"):
            system.set_max_history(0)
        
        with pytest.raises(ValueError, match="max_history must be positive"):
            system.set_max_history(-1)
    
    def test_max_history_enforcement(self):
        """Test that max history is enforced."""
        system = UndoRedoSystem(max_history=3)
        
        # Add more actions than max history
        for i in range(5):
            system.execute_action(f"action{i}", lambda: None, lambda x: None)
        
        # Should only keep the last 3 actions
        assert len(system._history) == 3
        assert system._current_position == 2
        
        # Check that oldest actions were removed
        names = system.get_action_names()
        assert names == ["action2", "action3", "action4"]
    
    def test_action_timestamp(self):
        """Test that actions have proper timestamps."""
        system = UndoRedoSystem()
        
        before_time = time.time()
        system.execute_action("action1", lambda: None, lambda x: None)
        after_time = time.time()
        
        action = system.get_current_action()
        assert before_time <= action.timestamp <= after_time
    
    def test_complex_scenario(self):
        """Test a complex scenario with multiple operations."""
        system = UndoRedoSystem(max_history=5)
        
        # Simulate a text editor
        text = ""
        
        def add_text(new_text):
            nonlocal text
            old_text = text
            text += new_text
            return old_text
        
        def remove_text(old_text):
            nonlocal text
            text = old_text
        
        # Execute actions
        system.execute_action("Add 'Hello'", lambda: add_text("Hello"), lambda old: remove_text(old))
        system.execute_action("Add ' '", lambda: add_text(" "), lambda old: remove_text(old))
        system.execute_action("Add 'World'", lambda: add_text("World"), lambda old: remove_text(old))
        system.execute_action("Add '!'", lambda: add_text("!"), lambda old: remove_text(old))
        
        assert text == "Hello World!"
        assert len(system._history) == 4
        
        # Undo some actions
        system.undo()
        system.undo()
        assert text == "Hello "
        
        # Redo one action
        system.redo()
        assert text == "Hello World"
        
        # Execute new action (should clear redo history)
        system.execute_action("Add '?'", lambda: add_text("?"), lambda old: remove_text(old))
        assert text == "Hello World?"
        assert not system.can_redo()
        
        # Undo all actions
        system.undo_multiple(4)
        assert text == ""
        assert system._current_position == -1
    
    def test_edge_cases(self):
        """Test various edge cases."""
        system = UndoRedoSystem(max_history=1)
        
        # Test with actions that return different types
        system.execute_action("int_action", lambda: 42, lambda x: None)
        system.execute_action("string_action", lambda: "hello", lambda x: None)
        system.execute_action("list_action", lambda: [1, 2, 3], lambda x: None)
        
        # Should only keep the last action due to max_history=1
        assert len(system._history) == 1
        assert system.get_current_action().name == "list_action"
        
        # Test with None values
        system.clear_history()
        system.execute_action("none_action", lambda: None, lambda x: None)
        
        action = system.get_current_action()
        assert action.name == "none_action"
        assert action.do_action() is None 