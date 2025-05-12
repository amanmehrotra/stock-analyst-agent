import json
import requests

from utils.config import google_translate_url, translation_key


# Send to API and get parsed response
def translate(text):
    payload = [[[text], "en", "hi"], "wt_lib"]
    print(json.dumps(payload))
    headers = {"Content-Type": "application/json+protobuf",
               "X-Goog-API-Key": translation_key}
    response = requests.post(google_translate_url, data=json.dumps(payload), headers=headers)

    if response.status_code == 200:
        try:
            translated = json.loads(response.text)
            # Extract from [[["..."]], "en", "hi"]
            return translated[0][0]
        except Exception as e:
            print("Error parsing response:", e)
            return text
    else:
        print(f"Error from API: {response.status_code}")
        return text

def initiate_translation(request):
    # Translate each news item
    delimiter = "~|~"
    for news_item in request.get("news", []):
        # input_text = f"{news_item.get('title','')}{delimiter}{news_item.get('summary','')}{delimiter}{news_item.get('sentiment','')}"
        # translated_text = translate(input_text)
        #
        # parts = translated_text.split(delimiter)
        # if len(parts) == 3:
        #     news_item["title"], news_item["summary"], news_item["sentiment"] = parts
        # else:
        #     print("Unexpected split result for news:", parts)
        news_item['title'] = translate(news_item['title'])
        news_item['summary'] = translate(news_item['summary'])
        news_item['sentiment'] = translate(news_item['sentiment'])

    # Translate indicator_explanation
    request["indicator_explanation"] = translate(request.get("indicator_explanation", ""))

    # Translate final_recommendation
    request["final_recommendation"] = translate(request.get("final_recommendation", ""))

    # Output the modified data
    # print("\n=== Final Translated Data ===")
    # print(json.dumps(request, indent=2, ensure_ascii=False))
    return request

# if __name__ == "__main__":
#     # Input JSON
#     data = {
#         "news": [
#             {"id": 1, "title": "SBI profits surge", "summary": "SBI reports 30% rise in net profits.",
#              "sentiment": "positive"},
#             {"id": 2, "title": "SBI faces scrutiny", "summary": "RBI questions SBI on compliance issues.",
#              "sentiment": "negative"}
#         ],
#         "indicator_explanation": "SMA and MACD show bullish trends while RSI is overbought.",
#         "final_recommendation": "Buy for intraday with entry at 803.3, target at 810, stoploss at 795."
#     }
#     initiate_translation(data)