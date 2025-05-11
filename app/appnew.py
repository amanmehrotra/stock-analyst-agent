import json
from datetime import datetime

import streamlit as st

from langgraph_flow.graph_builder import run_graph

def sentiment_color(sentiment):
    sentiment_display = {
        "positive": ("✅ Positive", "✅ सकारात्मक", "green"),
        "negative": ("🔴 Negative","🔴 नकारात्मक", "red"),
        "neutral": ("⚪ Neutral","⚪ तटस्थ", "gray"),
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
    st.title("📈 AM0002- Stock Analyst Agent")
    st.markdown("Intraday and Short-Term Trading Advisor")

    # Sidebar: Stock Selection
    stock_name = st.sidebar.selectbox(
        "Select a Stock",
        ["Indian Bank", "Adani Power", "PNB","IIFL","JSW Steel","Adani Green","IndusInd Bank","POWERGRID",
         "NTPC", "Ambuja Cement", "ATGL", "AWL Agri Business", "Adani Ports",
         "PAYTM", "Adani Enterprises", "IDEA", "SAIL", "BHEL", "BANK OF BARODA",
         "RVNL","ONGC", "SBI"]
    )

    trading_type = st.sidebar.selectbox(
        "Select Trading Type",
        ["Intraday", "Short-term"],
        index=0
    )

    language = st.sidebar.radio("Choose Language", ["hindi","english"], horizontal=True)

    if "result_json" not in st.session_state:
        st.session_state.result_json = None
    if "result" not in st.session_state:
        st.session_state.result = None
    if "result_json_hindi" not in st.session_state:
        st.session_state.result_json_hindi = None
    # Fetch Button
    analyze_button = st.sidebar.button("Analyze")
    if analyze_button:
        st.session_state.result_json = None

        with st.spinner("Fetching Stock news, chart indicators and analysis in progress..."):

            result = run_graph(stock_name, trading_type)
            result_json = result.get('analysis', None)
            result_json_hindi = result.get('analysis_hindi',None)
            if result_json is None or result_json_hindi is None:
                st.session_state.result_json = None
                st.session_state.result_json_hindi = None
                if language == "english":
                    st.info('Agent is busy at the moment. Please try again.')
                elif language == "hindi":
                    st.info('एजेंट इस समय व्यस्त है। कृपया पुनः प्रयास करें।')

            st.session_state.result_json = result_json
            st.session_state.result = result
            st.session_state.result_json_hindi = result_json_hindi
    elif analyze_button is False and st.session_state.result_json is None:
        if language == "hindi":
            st.info("कृपया एक स्टॉक चुनें और 'Analyze' पर क्लिक करें।")
        else:
            st.info("Please select a stock and click on 'Analyze'.")



    if st.session_state.result_json and st.session_state.result_json_hindi:
        result_json = st.session_state.result_json
        result = st.session_state.result
        result_json_hindi = st.session_state.result_json_hindi
        st.subheader(f"Analysis for: {result['stock_name']}")
        tab1, tab2, tab3 = st.tabs(["📰 News", "📊 Chart Indicators", "📜 Final Recommendation"])
        with tab2:
            st.markdown("### Chart Indicators")
            indicator_explanation = result_json.get('indicator_explanation_english','')
            indicators_org = result['indicators']
            col1, col2 = st.columns([2, 1])
            with col1:
                if result['chart_buffer']:
                    st.image(result['chart_buffer'], caption="📊 Stock Chart")
            with col2:
                col3, col4 = st.columns(2)
                with col3:
                    st.metric("Close Price", f"₹{indicators_org['close_price']}")
                    st.metric("SMA 20", f"₹{indicators_org['SMA_20']}")
                    st.metric("SMA 50", f"₹{indicators_org['SMA_50']}")
                    st.metric("RSI", f"{indicators_org['RSI']}")
                with col4:
                    st.metric("MACD", f"{indicators_org['MACD']}")
                    st.metric("MACD Signal", f"{indicators_org['MACD_signal']}")
                    st.metric("Bollinger High", f"₹{indicators_org['bollinger_high_band']}")
                    st.metric("Bollinger Low", f"₹{indicators_org['bollinger_low_band']}")
            st.markdown("### Explanation")
            if language == "hindi":
                st.success(f"{result_json_hindi.get('indicator_explanation', '')}")
            else:
                st.success(f"{indicator_explanation}")
        with tab1:
            st.markdown("### Latest News")
            n = result_json_hindi['news']
            m = {}
            for item in n:
                m[item['id']] = item
            news = result["news"]

            if not news:
                if language == 'hindi':
                    st.warning("अभी कोई समाचार उपलब्ध नहीं है।")
                else:
                    st.warning("No news currently available!")
            else:
                for i in news:
                    source = i['source'].split(':')[0]
                    item = m[i['id']]
                    if language == "hindi":
                        pass
                        label_en, label_hi, color = sentiment_color(i['sentiment'])
                        with st.expander(f"📌 **{item.get('title','')} (📰 {source})**"):
                            st.write(f"📄 {item.get('summary','')}")
                            st.markdown(f"🧠 **भाव:** <span style='color:{color}'>{label_hi}</span>",
                                        unsafe_allow_html=True)
                            st.markdown(f"🔗 [पूरा लेख पढ़ें]({i['link']})")
                            dt = datetime.strptime(i['publishedAt'], "%Y-%m-%d %H:%M:%S")
                            st.markdown(f"🕒 प्रकाशित: {dt.strftime("%b %d, %Y, %I:%M %p")}")

                    else:
                        label_en, label_hi, color = sentiment_color(i['sentiment'])
                        with st.expander(f"📌 **{i['title']} (📰 {source})**"):
                            st.write(f"📄 {i['summary']}")
                            st.markdown(f"🧠 **Sentiment:** <span style='color:{color}'>{label_en}</span>",
                                        unsafe_allow_html=True)
                            st.markdown(f"🔗 [Read article]({i['link']})")
                            dt = datetime.strptime(i['publishedAt'], "%Y-%m-%d %H:%M:%S")
                            st.markdown(f"🕒 Published on {dt.strftime("%b %d, %Y, %I:%M %p")}")
        with tab3:
            # Final Suggestion
            st.markdown("### Recommendation (AI-based)")
            if language == "hindi":
                st.success(f"{result_json_hindi.get('final_recommendation','')}")
            else:
                st.success(f"{result_json.get('final_recommendation_english','')}")