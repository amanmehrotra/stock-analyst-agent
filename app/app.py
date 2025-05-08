import streamlit as st
from app.ui import user_input
from langgraph_flow.graph_builder import run_graph

def start():
    st.title("📈"
             " Stock Analyst Agent (AM-0002)")
    stock_name = user_input()

    if st.button("Analyze"):
        #result = run_graph(stock_name)
        st.write("### 📜 Analysis (in Hindi):")
        #st.write(result['analysis_hindi'])
        st.write("### 📰 News Articles (Translated to Hindi):")
        # for i, article in enumerate(result['news_hindi'], 1):
        #     st.markdown(f"**{i}. {article}**")
        st.image("./services/chart.png", caption="📊 Stock Chart")
