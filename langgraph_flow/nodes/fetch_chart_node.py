from services.chart_fetcher import ChartService


def fetch_chart_node(state):
    chart_service = ChartService(state["stock_name"], state["trading_type"])
    df, buffer = chart_service.fetch_chart()
    df = chart_service.calculate_technical_indicators(df)
    indicators = chart_service.get_indicators(df)
    print(indicators)
    return {**state, "indicators": indicators, "chart_buffer": buffer}


# if __name__ == "__main__":
#     fetch_chart_node({"stock_name": "LIC", "trading_type": "3-6 Months"})