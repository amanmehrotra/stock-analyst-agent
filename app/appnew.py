import json
from datetime import datetime

import streamlit as st

from langgraph_flow.graph_builder import run_graph

def sentiment_color(sentiment):
    sentiment_display = {
        "positive": ("✅ Positive", "green"),
        "तटस्थ": ("⚪ तटस्थ", "gray"),
        "सकारात्मक": ("✅ सकारात्मक", "green"),
        "negative": ("🔴 Negative", "red"),
        "नकारात्मक": ("🔴 नकारात्मक", "red"),
        "neutral": ("⚪ Neutral", "gray"),
    }
    return sentiment_display[sentiment]


def start():

# Page config
    st.set_page_config(page_title="Stock Analyst - Intraday & Short-term", layout="wide")
### remove deploy button

    # st.markdown("""
    #     <style>
    #         /* Hide top toolbar including 'Deploy', 'Settings', 'Feedback' */
    #         [data-testid="stToolbar"] {
    #             display: none;
    #         }
    #
    #         /* Optionally hide the footer (Streamlit branding) */
    #         footer {
    #             visibility: hidden;
    #         }
    #     </style>
    # """, unsafe_allow_html=True)
    # Header
    st.title("📈 AM-0002: Stock Analyst Agent")
    st.markdown("Intraday and Short-Term Trading Advisor")

    # Sidebar: Stock Selection
    stock_name = st.sidebar.selectbox(
        "Select a Stock",
        ["Indian Bank", "Adani Power", "PNB","IIFL","POWERGRID",
         "NTPC", "Ambuja Cement", "ATGL", "AWL Agri Business", "Adani Ports",
         "PAYTM", "Adani Enterprises", "IDEA", "SAIL", "BHEL", "BANK OF BARODA",
         "RVNL","ONGC", "SBI"]
    )

    trading_type = st.sidebar.selectbox(
        "Select Trading Type",
        ["Intraday", "Short-term"],
        index=0
    )

    language = st.sidebar.radio("Choose Language", ["hindi", "english"], horizontal=True)

    if "result_json" not in st.session_state:
        st.session_state.result_json = None
    if "result" not in st.session_state:
        st.session_state.result = None
    # Fetch Button
    analyze_button = st.sidebar.button("Analyze")
    if analyze_button:
        st.session_state.result_json = None

        with st.spinner("Fetching Stock news, chart indicators and analysis in progress..."):

            result = run_graph(stock_name, trading_type)
            print(f"******************{result}")
            result_json = json.loads(result['analysis'])
            st.session_state.result_json = result_json
            st.session_state.result = result
    elif analyze_button is False and st.session_state.result_json is None:
        if language == "hindi":
            st.info("कृपया एक स्टॉक चुनें और 'Analyze' पर क्लिक करें।")
        else:
            st.info("Please select a stock and click on 'Analyze'.")



    if st.session_state.result_json:
        result_json = st.session_state.result_json
        result = st.session_state.result
        st.subheader(f"Analysis for: {stock_name}")
        tab1, tab2, tab3 = st.tabs(["📰 News", "📊 Chart Indicators", "📜 Recommendations"])
        with tab2:
            st.markdown("### Chart Indicators")
            indicators = result_json["indicator_analysis"]
            col1, col2 = st.columns([2, 1])
            with col1:
                st.image("chart.png", caption="📊 Stock Chart")
            with col2:
                col3, col4 = st.columns(2)
                with col3:
                    st.metric("Close Price", f"₹{indicators['close_price']}")
                    st.metric("SMA 20", f"₹{indicators['SMA_20']}")
                    st.metric("SMA 50", f"₹{indicators['SMA_50']}")
                    st.metric("RSI", f"{indicators['RSI']}")
                with col4:
                    st.metric("MACD", f"{indicators['MACD']}")
                    st.metric("MACD Signal", f"{indicators['MACD_signal']}")
                    st.metric("Bollinger High", f"₹{indicators['bollinger_high_band']}")
                    st.metric("Bollinger Low", f"₹{indicators['bollinger_low_band']}")
            st.markdown("### Explanation")
            if language == "hindi":
                st.success(f"{indicators['explanation_hindi']}")
            else:
                st.success(f"{indicators['explanation_english']}")
        with tab1:
            st.markdown("### Latest News")
            n = result_json["combined_news"]
            m = {}
            for item in n:
                m[item['id']] = item
            news = result["news"]
            # news = [
            #     {"title": "Indian Bank sees Q4 profit rise", "summary": "भारतीय बैंक का मुनाफा चौथी तिमाही में बढ़ा।"},
            #     {"title": "Indian Bank partners with NPCI", "summary": "भारतीय बैंक ने NPCI के साथ साझेदारी की।"},
            #     {"title": "Stock movement alert", "summary": "भारतीय बैंक के शेयर में उतार-चढ़ाव देखा गया।"},
            # ]
            print(news)
            if not news:
                st.warning("News not available")
            else:
                for i in news:
                    item = m[i['id']]
                    if language == "hindi":
                        label, color = sentiment_color(item['sentiment_hindi'])
                        with st.expander(f"**{item['title_hindi']}**"):
                            st.write(item['summary_hindi'])
                            st.markdown(f"**भाव:** <span style='color:{color}'>{label}</span>",
                                        unsafe_allow_html=True)
                            st.markdown(f"[पूरा लेख पढ़ें]({i['link']})")
                            dt = datetime.strptime(i['publishedAt'], "%Y-%m-%d %H:%M:%S")
                            st.markdown(f"प्रकाशित: {dt.strftime("%b %d, %Y, %I:%M %p")}")

                    else:
                        label, color = sentiment_color(item['sentiment_english'])
                        with st.expander(f"**{item['title_english']}**"):
                            st.write(item['summary_english'])
                            st.markdown(f"**Sentiment:** <span style='color:{color}'>{label}</span>",
                                        unsafe_allow_html=True)
                            st.markdown(f"[Read article]({i['link']})")
                            dt = datetime.strptime(i['publishedAt'], "%Y-%m-%d %H:%M:%S")
                            st.markdown(f"Published on {dt.strftime("%b %d, %Y, %I:%M %p")}")
        with tab3:
            # Final Suggestion
            st.markdown("### Recommendation (AI-based)")
            if language == "hindi":
                st.success(f"{result_json['final_recommendation_hindi']}")
            else:
                st.success(f"{result_json['final_recommendation_english']}")