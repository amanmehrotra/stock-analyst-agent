import json
from datetime import datetime

import yaml

from chains.analysis_chain import LLMService
from services import translator_service


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
    for item in llm_news:
        llm_news_map[item['id']] = (item["sentiment_english"],item["is_related_to_stock"])
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

    translate_request.indicator_explanation = state["analysis"].get("indicator_explanation_english",'')
    translate_request.final_recommendation = state["analysis"].get('final_recommendation_english','')
    # print(full_news_list)
    # translate_request_yaml = yaml.dump(translate_request.to_dict(), sort_keys=False, allow_unicode=True)
    # translate_request_json = json.dumps(translate_request.to_dict())
    #print(translate_request_json)
    # llm_service = LLMService(model_temperature=0.3)
    # analysis_hindi = llm_service.translate_to_hindi(translate_request_json)
    # print(analysis_hindi)
    # print(full_news_list)
    # Sort by 'publishedAt' in descending order
    full_news_list = sorted(
        full_news_list,
        key=lambda x: datetime.strptime(x['publishedAt'], '%Y-%m-%d %H:%M:%S'),
        reverse=True
    )

    analysis_hindi = translator_service.initiate_translation(translate_request.to_dict())
    return {**state, "news":full_news_list, "analysis_hindi": analysis_hindi}
