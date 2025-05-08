from services.translator import translate_to_hindi

def translate_node(state):
    news_hindi = [translate_to_hindi(article) for article in state["news"]]
    analysis_hindi = translate_to_hindi(state["analysis"])
    return {"news_hindi": news_hindi, "analysis_hindi": analysis_hindi}
