import logging
from typing import List

from langchain.tools import tool

logger = logging.getLogger(__name__)


class MathTools:

    def __init__(self):
        self.history = []

    def _diff_values(self, a: int, b: int) -> int:
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def _sum_values(self, a: int, b: int) -> int:
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def _get_history(self) -> str:
        if not self.history:
            return "No previous operations"
        return "\n".join(self.history[-5:])  # Last 5

    def get_tools(self) -> List:
        @tool
        def diff_values(a: int, b: int) -> int:
            """Calculates the difference between two numbers
            Args:
                a (int): first number
                b (int): second number
            Returns:
                int: difference of a - b
            """
            logger.info(f"Calculating difference: {a} - {b}")
            return self._diff_values(a, b)

        @tool
        def sum_values(a: int, b: int) -> int:
            """Sums two numbers
            Args:
                a (int): first number
                b (int): second number
            Returns:
                int: sum of a + b
            """
            logger.info(f"Calculating sum: {a} + {b}")
            return self._sum_values(a, b)

        @tool
        def get_history() -> str:
            """Gets the operation history
            Returns:
                str: last operations
            """
            logger.info("Retrieving operation history")
            return self._get_history()

        return [diff_values, sum_values, get_history]
