from mcp.server.fastmcp import FastMCP

from agents.data_analyst_agent import data_analyst_agent
from agents.document_agent import document_assistant_agent
from agents.ml_expert_agent import ml_expert_agent

mcp = FastMCP("RetailMind AI MCP Server")


@mcp.tool()
def data_analyst_tool(question: str) -> dict:
    """
    Retail analytics questions.
    Example:
    Which category has highest revenue?
    """
    return data_analyst_agent(question)


@mcp.tool()
def document_assistant_tool(question: str) -> dict:
    """
    Retail policy and customer support questions using RAG.
    Example:
    What is the refund policy?
    """
    return document_assistant_agent(question)


@mcp.tool()
def ml_expert_tool(question: str) -> dict:
    """
    ML forecasting and anomaly explanation.
    Example:
    Explain the forecasting model.
    """
    return ml_expert_agent(question)


if __name__ == "__main__":
    print("RetailMind AI MCP Server is running...")
    mcp.run()