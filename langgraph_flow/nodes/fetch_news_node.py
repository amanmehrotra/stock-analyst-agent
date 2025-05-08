from services.newsapi_service import NewsApiService

def fetch_news_node(state):
    news_service = NewsApiService()
    news_list = news_service.fetch_recent_news_from_rss(state['stock_name'])
    # for news in news_list[0:5]:
    #     print(f"Title: {news['title']}")
    #     print(f"Summary: {news['summary']}")
    #     print(f"Link: {news['link']}")
    #     print(f"Published: {news['published']}")
    #     print("-" * 80)
    # print(f"**********{news_list}")
    return {**state, "news": news_list}
