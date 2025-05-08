import requests
from config.settings import NEWS_API_KEY
import feedparser
from datetime import datetime, timedelta

from utils.config import ET_FEEDS


class NewsApiService:

    def fetch_recent_news_from_rss(self, stock_name, days=5):
        seen_urls = set()
        news_items = []
        for feed_name, url in ET_FEEDS.items():
            feed = feedparser.parse(url)
            # feed = feedparser.parse(self.url)


            cutoff_date = datetime.now() - timedelta(days=days)
            #print(f"********{feed["entries"]}")
            id=1
            for entry in feed.entries:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                published_parsed = entry.get("published_parsed")
                url = entry.link
                if published_parsed:
                    published_date = datetime(*published_parsed[:6])
                    if published_date >= cutoff_date:
                        if stock_name.lower() in title.lower() or stock_name.lower() in summary.lower():
                            if url not in seen_urls:
                                news_items.append({
                                    "id": id,
                                    "title": title,
                                    "summary": summary,
                                    "link": entry.get("link"),
                                    "publishedAt": published_date.strftime("%Y-%m-%d %H:%M:%S"),
                                    "source": feed_name
                                })
                                id=id+1
                                seen_urls.add(url)

        return news_items

    # def fetch_news(self, stock_name):
    #     url = self.url
    #     params = {
    #         "q": stock_name,
    #         "apiKey": self.api_key,
    #         "pageSize": 5,
    #         "sortBy": "publishedAt",
    #         "language": "en"
    #     }
    #
    #     response = requests.get(url, params=params, headers=self.headers)
    #     articles = response.json().get("articles", [])
    #     return [article["title"] for article in articles]

# if __name__ == "__main__":
#     news_service = NewsApiService("Adani Power")
#     news_service.fetch_recent_news_from_rss("Adani Power")