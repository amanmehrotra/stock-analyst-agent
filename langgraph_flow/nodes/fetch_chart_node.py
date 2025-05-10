from services.chart_fetcher import ChartService


def fetch_chart_node(state):
    chart_service = ChartService(state["stock_name"], state["trading_type"])
    df, buffer = chart_service.fetch_chart()
    df = chart_service.calculate_technical_indicators(df)
    indicators = chart_service.get_indicators(df)
    return {**state, "indicators": indicators, "chart_buffer": buffer}
