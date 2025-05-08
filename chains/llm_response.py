from pydantic import BaseModel
from typing import List, Literal

class NewsItem(BaseModel):
    id: int
    title_hindi: str
    title_english: str
    summary_hindi: str
    summary_english: str
    sentiment_english: Literal["positive", "negative", "neutral"]
    sentiment_hindi: Literal["सकारात्मक", "नकारात्मक", "तटस्थ"]

class IndicatorAnalysis(BaseModel):
    close_price: str
    SMA_20: str
    SMA_50: str
    RSI: str
    MACD: str
    MACD_signal: str
    bollinger_low_band: str
    bollinger_high_band: str
    explanation_hindi: str
    explanation_english: str

class StockAnalysisOutput(BaseModel):
    combined_news: List[NewsItem]
    indicator_analysis: IndicatorAnalysis
    final_recommendation_hindi: str
    final_recommendation_english: str
