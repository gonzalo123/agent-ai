"""
Unit tests for the prompts module
"""

import pytest


class TestPrompts:
    """Test cases for prompt configurations"""

    def test_agent_system_prompt_exists(self):
        """Test that AGENT_SYSTEM_PROMPT is defined"""
        from modules.prompts import AGENT_SYSTEM_PROMPT

        assert AGENT_SYSTEM_PROMPT is not None
        assert isinstance(AGENT_SYSTEM_PROMPT, str)
        assert len(AGENT_SYSTEM_PROMPT) > 0

    def test_agent_system_prompt_content(self):
        """Test AGENT_SYSTEM_PROMPT contains expected content"""
        from modules.prompts import AGENT_SYSTEM_PROMPT

        # Check for key phrases that should be in the prompt
        assert "mathematical agent" in AGENT_SYSTEM_PROMPT.lower()
        assert "calculations" in AGENT_SYSTEM_PROMPT.lower()
        assert "tools" in AGENT_SYSTEM_PROMPT.lower()

    def test_prompt_mentions_available_tools(self):
        """Test that prompt mentions the available tools"""
        from modules.prompts import AGENT_SYSTEM_PROMPT

        assert "diff_values" in AGENT_SYSTEM_PROMPT
        assert "sum_values" in AGENT_SYSTEM_PROMPT
        assert "get_history" in AGENT_SYSTEM_PROMPT

    def test_prompt_contains_guidelines(self):
        """Test that prompt contains usage guidelines"""
        from modules.prompts import AGENT_SYSTEM_PROMPT

        assert "Guidelines:" in AGENT_SYSTEM_PROMPT
        assert "mathematical operations" in AGENT_SYSTEM_PROMPT.lower()

    def test_prompt_mentions_complex_operations(self):
        """Test that prompt mentions complex operations handling"""
        from modules.prompts import AGENT_SYSTEM_PROMPT

        assert "complex operations" in AGENT_SYSTEM_PROMPT.lower()
        assert "step-by-step" in AGENT_SYSTEM_PROMPT.lower()

    def test_prompt_mentions_arithmetic_operations(self):
        """Test that prompt mentions specific arithmetic operations"""
        from modules.prompts import AGENT_SYSTEM_PROMPT

        operations = ["multiplication", "division", "exponentiation", "square root"]
        for operation in operations:
            assert operation.lower() in AGENT_SYSTEM_PROMPT.lower()

    def test_prompt_structure_is_well_formatted(self):
        """Test that prompt is well-formatted with proper structure"""
        from modules.prompts import AGENT_SYSTEM_PROMPT

        # Check for basic structure elements
        lines = AGENT_SYSTEM_PROMPT.strip().split("\n")
        assert len(lines) > 5  # Should have multiple lines

    def test_prompt_language_is_english(self):
        """Test that prompt is written in English"""
        from modules.prompts import AGENT_SYSTEM_PROMPT

        # Check that prompt doesn't contain Spanish keywords
        spanish_words = ["calculadora", "matemático", "operaciones", "suma", "resta"]
        for word in spanish_words:
            assert word not in AGENT_SYSTEM_PROMPT.lower()

    def test_prompt_immutability(self):
        """Test that prompt constant behavior"""
        # Import again to ensure it's the same
        import importlib

        import modules.prompts
        from modules.prompts import AGENT_SYSTEM_PROMPT

        importlib.reload(modules.prompts)

        from modules.prompts import AGENT_SYSTEM_PROMPT as PROMPT_2

        assert AGENT_SYSTEM_PROMPT == PROMPT_2
