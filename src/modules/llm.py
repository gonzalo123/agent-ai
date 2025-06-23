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
