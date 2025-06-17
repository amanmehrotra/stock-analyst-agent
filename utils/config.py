import os
import streamlit as st

#ET Feeds URL
ET_FEEDS = {
    "The Economic Times:Markets": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "The Economic Times:Stock Market": "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
    "The Economic Times:Banking-Finance": "https://economictimes.indiatimes.com/industry/banking/finance/rssfeeds/13358259.cms",
    "The Economic Times:Economy": "https://economictimes.indiatimes.com/news/economy/rssfeeds/137338068.cms",
    "The Economic Times:Industry": "https://economictimes.indiatimes.com/industry/rssfeeds/13352306.cms",
    "Business-Standard:business-Markets": "https://www.business-standard.com/rss/markets-106.rss",
    "Business-Standard:business-Economy": "https://www.business-standard.com/rss/economy-102.rss",
    "Business-Standard:business-Industry": "https://www.business-standard.com/rss/industry-217.rss",
    "Business-Standard:Finance": "https://www.business-standard.com/rss/finance-103.rss",
    "Business-Standard:Companies": "https://www.business-standard.com/rss/companies-101.rss",
    "Business-Standard:Top-News": "https://www.business-standard.com/rss/home_page_top_stories.rss",

    "Business-Standard:Companies-news": "https://www.business-standard.com/rss/companies/news-10101.rss",
    "Business-Standard:Stock-market-news": "https://www.business-standard.com/rss/markets/stock-market-news-10618.rss",
    "Business-Standard:Market-news": "https://www.business-standard.com/rss/markets/news-10601.rss",
    "Business-Standard:Finance-news": "https://www.business-standard.com/rss/finance/news-10301.rss",
    "Business-Standard:Economy-news": "https://www.business-standard.com/rss/economy/news-10201.rss"
}

# OpenAI variables
#llm_baseurl = "https://openrouter.ai/api/v1"
llm_baseurl = "https://api.groq.com/openai/v1"
llm_key = st.secrets["GROQ_API_KEY"]
#llm_model = "llama3-70b-8192"
llm_model="llama-3.3-70b-versatile"
# google translation API
google_translate_url = "https://translate-pa.googleapis.com/v1/translateHtml"
translation_key = st.secrets["TRANSLATION_API_KEY"]
