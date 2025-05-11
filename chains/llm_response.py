from pydantic import BaseModel
from typing import List, Literal, Optional


class NewsItem(BaseModel):
    id: int
    title_hindi: Optional[str] = None
    title_english: str
    summary_hindi: Optional[str] = None
    summary_english: str
    is_related_to_stock: str
    sentiment_english: Literal["positive", "negative", "neutral"]
    sentiment_hindi: Optional[str] = None

class IndicatorAnalysis(BaseModel):
    close_price: str
    SMA_20: str
    SMA_50: str
    RSI: str
    MACD: str
    MACD_signal: str
    bollinger_low_band: str
    bollinger_high_band: str
    explanation_hindi: Optional[str] = None
    explanation_english: str

class StockAnalysisOutput(BaseModel):
    combined_news: List[NewsItem]
    indicator_analysis: IndicatorAnalysis
    final_recommendation_hindi: Optional[str] = None
    final_recommendation_english: str
