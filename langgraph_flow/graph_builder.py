from io import BytesIO
from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END
from langgraph_flow.nodes.input_node import input_node
from langgraph_flow.nodes.fetch_news_node import fetch_news_node
from langgraph_flow.nodes.fetch_chart_node import fetch_chart_node
from langgraph_flow.nodes.analyze_node import analyze_node
from langgraph_flow.nodes.translate_node import translate_node

class StateModel(TypedDict):
    stock_name: str
    trading_type: str
    news: list
    indicators: object
    analysis: object
    chart_buffer: Optional[BytesIO]
def run_graph(stock_name, trading_type):
    builder = StateGraph(StateModel)

    builder.add_node("input", input_node)
    builder.add_node("fetch_news", fetch_news_node)
    builder.add_node("fetch_chart", fetch_chart_node)
    builder.add_node("analyze", analyze_node)
    # builder.add_node("translate", translate_node)

    builder.set_entry_point("input")
    builder.add_edge("input", "fetch_news")
    builder.add_edge("fetch_news", "fetch_chart")
    builder.add_edge("fetch_chart", "analyze")
    # builder.add_edge("analyze", "translate")
    builder.add_edge("analyze", END)

    graph = builder.compile()
    return graph.invoke({"stock_name": stock_name, "trading_type": trading_type})
