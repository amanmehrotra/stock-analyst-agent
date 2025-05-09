import json

from langchain_core.messages.tool import tool_call
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from chains.llm_response import StockAnalysisOutput
from chains.prompt import PROMPT
from utils.config import llm_baseurl, llm_key, llm_model
from langchain.output_parsers import PydanticOutputParser

class LLMService:
    def __init__(self):
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
            temperature=0.3
)

    def analyze_news_and_chart(self, stock_name, news, indicators, trading_type):
        # news_summary = "\n".join(news_list)

        # Set up the parser with the output schema
        parser = PydanticOutputParser(pydantic_object=StockAnalysisOutput)

        prompt = PromptTemplate.from_template(PROMPT)
        format_instructions = parser.get_format_instructions()
        print(format_instructions)
        chain = prompt | self.llm | parser
        # chain = prompt | self.llm
        try:
            feedback = chain.invoke({"stock_name": stock_name,
                                     "news_json": news,
                                     "indicators_json": indicators,
                                     "trading_type": trading_type,
                                     "format_instructions": format_instructions})

            print(feedback)
            return feedback
        except Exception as e:
            print(e)
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