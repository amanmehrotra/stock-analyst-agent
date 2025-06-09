import json

from chains.analysis_chain import LLMService


def analyze_node(state):
    llm_service = LLMService(model_temperature=0.2)
    news_json = json.dumps(state["news"])
    indicators_json = json.dumps(state["indicators"])
    analysis = llm_service.analyze_news_and_chart(state["stock_name"], news_json, indicators_json,
                                                  state["trading_type"])
    return {**state, "analysis": analysis}
