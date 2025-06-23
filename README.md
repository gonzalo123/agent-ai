# Building an AI Agent with LangChain, AWS Bedrock and Claude 4 Sonnet

Today we are going to build an agent with IA. It is just an example of how to build a agent with LangChain and AWS Bedrock and Claude 4 Sonnet. The agent will be a "mathematical expert" capable of performing complex calculations and providing detailed explanations of its reasoning process. The idea is to provide the agent with the ability to perform mathematical operations like addition, subtraction. In fact, with additions and subtractions, we can perform all the mathematical operations, like multiplication, division, exponentiation, square root, etc. The agent will be able to perform these operations step by step, providing a detailed explanation of its reasoning process. I know that we don't need to use AI to perform these operations, but the idea is to show how to build an agent with LangChain and AWS Bedrock and Claude 4 Sonnet.

The mathematical agent implements the tool-calling pattern, allowing the LLM to dynamically select and execute mathematical operations:

```python
import logging

from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate

from core.llm.aws import get_llm, Models
from modules.prompts import AGENT_SYSTEM_PROMPT
from modules.tools import MathTools
from settings import MAX_TOKENS

logger = logging.getLogger(__name__)


def run(question: str, model: Models = Models.CLAUDE_4):
    prompt = ChatPromptTemplate.from_messages([
        ("system", AGENT_SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    math_tools = MathTools()
    tools = math_tools.get_tools()

    llm = get_llm(model=model, max_tokens=MAX_TOKENS)
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=10
    )

    response = agent_executor.invoke({
        "input": question
    })

    logger.info(f"Agent response: {response['output']}")
```

Tools are defined using LangChain's `@tool` decorator, providing automatic schema generation and type validation. Really we don't need to create a class for the tools, but I have done it because I want to add an extra feature to the agent: the ability to keep a history of the operations performed. This will allow the agent to provide a detailed explanation of its reasoning process, showing the steps taken to arrive at the final result.

```python
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
```

The system prompt is carefully crafted to guide the agent's behavior and establish clear operational boundaries:

```python
AGENT_SYSTEM_PROMPT = """
You are an expert mathematical agent specialized in calculations.

You have access to the following tools:
- diff_values: Calculates the difference between two numbers
- sum_values: Sums two numbers
- get_history: Gets the operation history

Guidelines:
1. Only answer questions related to mathematical operations.
2. For complex operations, use step-by-step calculations:
   - Multiplication: Repeated addition
   - Division: Repeated subtraction
   - Exponentiation: Repeated multiplication
   - Square root: Use methods like Babylonian method or prime factorization.
"""
```

And that's all. This project demonstrates how to build a production-ready AI agent using LangChain and AWS Bedrock. It's just a boilerplate, but it can be extended to create more complex agents with additional capabilities and understand how AI agents works