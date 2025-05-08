import os
import streamlit as st

#ET Feeds URL
ET_FEEDS = {
    "Top News": "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
    "Markets": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "Stock Market": "https://economictimes.indiatimes.com/markets/stocks/rssfeeds/2146842.cms",
    "Banking/Finance": "https://economictimes.indiatimes.com/industry/banking/finance/rssfeeds/13358259.cms",
    "Economy": "https://economictimes.indiatimes.com/news/economy/rssfeeds/137338068.cms",
    "Industry": "https://economictimes.indiatimes.com/industry/rssfeeds/13352306.cms"
}

# OpenAI variables
llm_baseurl = "https://openrouter.ai/api/v1"
llm_key = st.secrets["OPENROUTER_API_KEY"]