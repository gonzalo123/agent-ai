"""
Unit tests for the MathTools module
"""

from unittest.mock import Mock, patch

import pytest


class TestMathTools:
    """Test cases for MathTools class"""

    def test_math_tools_initialization(self, math_tools_instance):
        """Test MathTools initialization"""
        assert math_tools_instance.history == []

    def test_diff_values_calculation(self, math_tools_instance):
        """Test difference calculation"""
        result = math_tools_instance._diff_values(10, 3)

        assert result == 7
        assert len(math_tools_instance.history) == 1
        assert "10 - 3 = 7" in math_tools_instance.history[0]

    def test_sum_values_calculation(self, math_tools_instance):
        """Test sum calculation"""
        result = math_tools_instance._sum_values(5, 8)

        assert result == 13
        assert len(math_tools_instance.history) == 1
        assert "5 + 8 = 13" in math_tools_instance.history[0]

    def test_negative_numbers_diff(self, math_tools_instance):
        """Test difference with negative numbers"""
        result = math_tools_instance._diff_values(-5, -2)

        assert result == -3
        assert "-5 - -2 = -3" in math_tools_instance.history[0]

    def test_negative_numbers_sum(self, math_tools_instance):
        """Test sum with negative numbers"""
        result = math_tools_instance._sum_values(-3, 7)

        assert result == 4
        assert "-3 + 7 = 4" in math_tools_instance.history[0]

    def test_get_history_empty(self, math_tools_instance):
        """Test get_history when no operations performed"""
        result = math_tools_instance._get_history()

        assert result == "No previous operations"

    def test_get_history_with_operations(self, math_tools_instance):
        """Test get_history with operations"""
        math_tools_instance._sum_values(1, 2)
        math_tools_instance._diff_values(5, 3)

        result = math_tools_instance._get_history()

        assert "1 + 2 = 3" in result
        assert "5 - 3 = 2" in result
        assert result.count("\n") == 1  # Two operations

    def test_get_history_limits_to_five(self, math_tools_instance):
        """Test that history is limited to last 5 operations"""
        # Perform 7 operations
        for i in range(7):
            math_tools_instance._sum_values(i, 1)

        result = math_tools_instance._get_history()
        lines = result.split("\n")

        assert len(lines) == 5  # Only last 5 operations
        assert "6 + 1 = 7" in result  # Last operation
        assert "0 + 1 = 1" not in result  # First operation should not be present

    def test_get_tools_returns_list(self, math_tools_instance):
        """Test that get_tools returns a list"""
        tools = math_tools_instance.get_tools()

        assert isinstance(tools, list)
        assert len(tools) == 3

    def test_tools_have_correct_names(self, math_tools_instance):
        """Test that tools have correct names"""
        tools = math_tools_instance.get_tools()
        tool_names = [tool.name for tool in tools]

        assert "diff_values" in tool_names
        assert "sum_values" in tool_names
        assert "get_history" in tool_names

    def test_diff_tool_functionality(self, math_tools_instance):
        """Test the diff tool created by get_tools"""
        tools = math_tools_instance.get_tools()
        diff_tool = next(tool for tool in tools if tool.name == "diff_values")

        result = diff_tool.func(15, 7)

        assert result == 8
        assert "15 - 7 = 8" in math_tools_instance.history[-1]

    def test_sum_tool_functionality(self, math_tools_instance):
        """Test the sum tool created by get_tools"""
        tools = math_tools_instance.get_tools()
        sum_tool = next(tool for tool in tools if tool.name == "sum_values")

        result = sum_tool.func(12, 18)

        assert result == 30
        assert "12 + 18 = 30" in math_tools_instance.history[-1]

    def test_history_tool_functionality(self, math_tools_instance):
        """Test the history tool created by get_tools"""
        # Add some operations first
        math_tools_instance._sum_values(1, 1)
        math_tools_instance._diff_values(5, 2)

        tools = math_tools_instance.get_tools()
        history_tool = next(tool for tool in tools if tool.name == "get_history")

        result = history_tool.func()

        assert "1 + 1 = 2" in result
        assert "5 - 2 = 3" in result

    def test_tools_have_docstrings(self, math_tools_instance):
        """Test that tools have proper docstrings"""
        tools = math_tools_instance.get_tools()

        for tool in tools:
            assert hasattr(tool, "description")
            assert len(tool.description) > 0

    def test_concurrent_instances_separate_history(self):
        """Test that different MathTools instances have separate histories"""
        from modules.tools import MathTools

        tools1 = MathTools()
        tools2 = MathTools()

        tools1._sum_values(1, 1)
        tools2._diff_values(5, 2)

        assert len(tools1.history) == 1
        assert len(tools2.history) == 1
        assert tools1.history[0] != tools2.history[0]
