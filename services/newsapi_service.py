import requests
from config.settings import NEWS_API_KEY
import feedparser
from datetime import datetime, timedelta

from utils.config import ET_FEEDS
from rapidfuzz import fuzz

class NewsApiService:

    def fetch_recent_news_from_rss(self, stock_name, days=30    ):
        seen_urls = set()
        news_items = []
        id_field = 1
        for feed_name, url in ET_FEEDS.items():
            headers = {
                "User-Agent": "PostmanRuntime/7.43.4",
            "Accept": "*/*",}
            # Fetch the RSS feed with custom headers
            response = requests.get(url, headers=headers)
            print(url)
            print("\n")
            if response.status_code == 200:
                # Parse the RSS feed
                feed = feedparser.parse(response.text)
            # feed = feedparser.parse(url)

                cutoff_date = datetime.now() - timedelta(days=days)
                #print(f"********{feed["entries"]}")

                for entry in feed.entries:
                    title = entry.get("title", "")
                    summary = entry.get("summary", "")
                    published_parsed = entry.get("published_parsed")
                    url = entry.link
                    if published_parsed:
                        published_date = datetime(*published_parsed[:6])
                        if published_date >= cutoff_date:
                            if is_news_relevant(title.lower(), summary.lower(), stock_name.lower(), threshold=85):
                            # if stock_name.lower() in title.lower() or stock_name.lower() in summary.lower():
                                if url not in seen_urls:
                                    news_items.append({
                                        "id": id_field,
                                        "title": title,
                                        "summary": summary,
                                        "link": entry.get("link"),
                                        "publishedAt": published_date.strftime("%Y-%m-%d %H:%M:%S"),
                                        "source": feed_name
                                    })
                                    id_field=id_field+1
                                    seen_urls.add(url)
        print(news_items)
        return news_items[:7]

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
#     news_service = NewsApiService()
#     news_service.fetch_recent_news_from_rss("Adani Power")

def is_news_relevant(news_title, news_description, stock_name, threshold=85):
    """Returns True if news is relevant to the given stock using NER and fuzzy match."""

    combined_text = f"{news_title} {news_description}"

    # Step 1: Fuzzy match with stock aliases
    aliases = STOCK_ALIASES.get(stock_name, [stock_name])
    for alias in aliases:
        if fuzz.partial_ratio(alias.lower(), combined_text.lower()) >= threshold:
            return True

    # Step 2: NER match with ORG entities
    # doc = nlp(combined_text)
    # org_entities = [ent.text.lower() for ent in doc.ents if ent.label_ == "ORG"]
    #
    # for org in org_entities:
    #     for alias in aliases:
    #         if fuzz.partial_ratio(alias.lower(), org) >= threshold:
    #             return True

    return False

STOCK_ALIASES = {
    "Indian Bank": ["Indian Bank", "PSU bank Indian Bank", "INDIANB"],
    "Adani Power": ["Adani Power", "Adani Power Ltd", "Adani electricity arm", "ADANIPOWER"],
    "PNB": ["PNB", "Punjab National Bank", "PSU lender PNB", "PNB"],
    "IIFL": ["IIFL", "India Infoline", "IIFL Finance", "IIFL"],
    "JSW Steel": ["JSW Steel", "JSW Group", "JSW", "JSWSTEEL"],
    "Adani Green": ["Adani Green", "Adani Green Energy", "Adani renewable arm", "ADANIGREEN"],
    "IndusInd Bank": ["IndusInd Bank", "Private lender IndusInd", "IndusInd", "INDUSINDBK"],
    "POWERGRID": ["POWERGRID", "Power Grid", "Power Grid Corp", "PGCIL"],
    "NTPC": ["NTPC", "National Thermal Power Corp", "NTPC Ltd"],
    "Ambuja Cement": ["Ambuja Cement", "Ambuja Cements Ltd", "Adani cement arm", "AMBUJACEM"],
    "ATGL": ["ATGL", "Adani Total Gas", "Adani gas arm"],
    "AWL Agri Business": ["AWL", "Adani Wilmar", "AWL Agri", "Adani FMCG arm"],
    "Adani Ports": ["Adani Ports", "Adani Ports and SEZ", "APSEZ", "ADANIPORTS"],
    "PAYTM": ["Paytm", "One97 Communications", "Paytm Payments", "Paytm stock", "PAYTM"],
    "Adani Enterprises": ["Adani Enterprises", "Adani Ent", "Adani flagship firm", "ADANIENT"],
    "IDEA": ["IDEA", "Vodafone Idea", "Vi", "Voda Idea"],
    "SAIL": ["SAIL", "Steel Authority of India", "SAIL Ltd"],
    "BHEL": ["BHEL", "Bharat Heavy Electricals"],
    "BANK OF BARODA": ["Bank of Baroda", "BoB", "PSU lender BoB", "BANKBARODA"],
    "RVNL": ["RVNL", "Rail Vikas Nigam Ltd", "Rail infra PSU RVNL"],
    "ONGC": ["ONGC", "Oil and Natural Gas Corp", "ONGC Ltd"],
    "SBI": ["SBI", "State Bank of India", "India’s largest bank SBI", "SBIN"],
    "Hindalco": ["Hindalco", "Hindalco Industries", "Aditya Birla metal arm", "HINDALCO"],
    "BEL": ["BEL", "Bharat Electronics", "Bharat Electronics Ltd"],
    "Canara Bank": ["Canara Bank", "PSU lender Canara", "Canara", "CANBK"],
    "Coal India": ["Coal India", "CIL", "Coal PSU", "COALINDIA"],
    "Indian Oil": ["Indian Oil", "IOC", "Indian Oil Corp"],
    "Indian Oil Finance": ["Indian Oil Finance", "IOC Finance", "IOCL bond arm"],
    "NBCC": ["NBCC", "National Buildings Construction Corp", "NBCC India"],
    "IRCON": ["IRCON", "IRCON International", "Rail PSU IRCON"],
    "Reliance": ["Reliance", "Reliance Industries", "RIL", "Mukesh Ambani firm", "RELIANCE"],
    "Renuka": ["Renuka", "Shree Renuka Sugars", "Renuka Sugars", "RENUKA"],
    "RAILTEL": ["RailTel", "RailTel Corp", "Rail PSU RailTel", "RAILTEL"],
    "LIC": ["LIC", "Life Insurance Corporation", "LIC India", "LICI"]
}
