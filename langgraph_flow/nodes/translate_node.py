import json
from datetime import datetime

from chains.analysis_chain import LLMService

class TranslateRequest:
    def __init__(self):
        self.news = []
        self.indicator_explanation:str = ''
        self.final_recommendation:str = ''

    def to_dict(self):
        return {
            "news": self.news,
            "indicator_explanation": self.indicator_explanation,
            "final_recommendation": self.final_recommendation
        }

def translate_node(state):
    news = []
    if state["analysis"] is None:
        return {**state, "analysis_hindi": None}

    llm_news = state["analysis"]["combined_news"]
    llm_news_map = {}
    for n in llm_news:
        llm_news_map[n['id']] = (n["sentiment_english"],n["is_related_to_stock"])
    full_news_list = []
    for record in state["news"]:
        # print(f"{record}***")
        if record['id'] in llm_news_map.keys():
            if llm_news_map[record['id']][1] == 'yes':
                record['sentiment'] = llm_news_map[record['id']][0]
                record_copy = dict(record)
                record_copy.pop('link')
                record_copy.pop('source')
                record_copy.pop('publishedAt')
                news.append(record_copy)
                full_news_list.append(record)
    translate_request = TranslateRequest()
    translate_request.news = news
    if "analysis" in state.keys() and "indicator_analysis" in state["analysis"].keys():
        translate_request.indicator_explanation = state["analysis"]["indicator_analysis"].get("explanation_english",'')
    if "analysis" in state.keys() and "final_recommendation_english" in state["analysis"].keys():
        translate_request.final_recommendation = state["analysis"]["final_recommendation_english"]
    # print(full_news_list)
    # translate_request_json = json.dumps(translate_request.to_dict())
    #print(translate_request_json)
    # llm_service = LLMService(model_temperature=0.4)
    # analysis_hindi = llm_service.translate_to_hindi(translate_request_json)
    # print(analysis_hindi)
    # print(full_news_list)
    # Sort by 'publishedAt' in descending order
    full_news_list = sorted(
        full_news_list,
        key=lambda x: datetime.strptime(x['publishedAt'], '%Y-%m-%d %H:%M:%S'),
        reverse=True
    )
    return {**state, "news":full_news_list}
