import json

import yaml
from groq import Groq
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from chains.llm_response import StockAnalysisOutput
from chains.prompt import PROMPT
from chains.translation_prompt import TRANSLATION_SYSTEM_PROMPT
from utils.config import llm_baseurl, llm_key, llm_model


class LLMService:
    def __init__(self, model_temperature):
        self.url = llm_baseurl
        # self.llm =  ChatOpenAI(
        #     model="deepseek/deepseek-r1:free",
        #     base_url=self.url,
        #     api_key=llm_key,
        #     temperature=0.3
        self.llm =  ChatOpenAI(
            model=llm_model,
            base_url=self.url,
            api_key=llm_key,
            temperature=model_temperature)
        self.client = Groq(api_key=llm_key)

        self.llm = self.llm.bind(response_format={"type": "json_object"})

    def analyze_news_and_chart(self, stock_name, news, indicators, trading_type):

        # Set up the parser with the output schema
        parser = PydanticOutputParser(pydantic_object=StockAnalysisOutput)

        prompt = PromptTemplate.from_template(PROMPT)
        format_instructions = parser.get_format_instructions()
        # print(format_instructions)
        chain = prompt | self.llm
        # chain = prompt | self.llm
        feedback = None
        try:
            feedback = chain.invoke({"stock_name": stock_name,
                                     "news_json": news,
                                     "indicators_json": indicators,
                                     "trading_type": trading_type})

            print(f"llm analysis content:{feedback}\n")
            return json.loads(feedback.content)
        except Exception as e:
            print(f"exception: {e}")
            return None

    def translate_to_hindi(self, translate_request_yaml):
        # prompt = PromptTemplate.from_template(TRANSLATION_PROMPT)
        # print(f"\n{translate_request_json}")
        # chain = prompt | self.llm
        # try:
        #     feedback = chain.invoke({"json_string": translate_request_json})
        #
        #     print(feedback)
        #     return json.loads(feedback.content)
        # except Exception as e:
        #     print(f"exception: {e}")
        #     return None
        try:
            completion = self.client.chat.completions.create(
                model=llm_model,
                messages=[
                    {"role": "system", "content": TRANSLATION_SYSTEM_PROMPT},
                    {"role": "user", "content": f"Translate the yaml {translate_request_yaml}"}
                ],
                temperature = 0.4
            )
            print(translate_request_yaml)
            response_content = completion.choices[0].message.content
            print(f"llm translation content: {response_content}\n")
            print(response_content)
            return validate_translated_yaml(response_content)
        except Exception as e:
            print(f"exception: {e}")
            return None


def validate_translated_yaml(yaml_str):
    try:
        data = yaml.safe_load(yaml_str)

        # Basic structure validation
        assert "news" in data and isinstance(data["news"], list), "Missing or invalid 'news'"
        for item in data["news"]:
            assert isinstance(item.get("id"), int), "News 'id' must be an integer"
            assert isinstance(item.get("title"), str), "News 'title' must be a string"
            assert isinstance(item.get("summary"), str), "News 'summary' must be a string"
            assert isinstance(item.get("sentiment"), str), "News 'sentiment' must be a string"

        assert isinstance(data.get("indicator_explanation"), str), "Missing or invalid 'indicator_explanation'"
        assert isinstance(data.get("final_recommendation"), str), "Missing or invalid 'final_recommendation'"

        print("YAML is valid.")
        return data

    except (yaml.YAMLError, AssertionError) as e:
        print("Invalid YAML or structure error:", str(e))
        return None

# if __name__ == "__main__":
#     news_articles = [
#         {
#             "title": "Tata Motors reports 20% increase in quarterly profit",
#             "summary": "Driven by strong domestic demand and EV sales.",
#             "publishedAt": "2025-05-04T10:30:00Z",
#             "url": "https://example.com/news1"
#         },
#         {
#             "title": "EV unit of Tata Motors gets $1 billion funding",
#             "summary": "Investment from global equity firm expected to boost R&D.",
#             "publishedAt": "2025-05-03T08:15:00Z",
#             "url": "https://example.com/news2"
#         }
#     ]
#
#     chart_indicators = {
#         "SMA": 890,
#         "RSI": 68,
#         "close_price": 920
#     }
#
#     news_json = json.dumps(news_articles),
#     indicators_json = json.dumps(chart_indicators)
#     llmService = LLMService()
#     llmService.analyze_news_and_chart("Tata motors", news_json, indicators_json)