# tool/sentiment.py - Using TextBlob
from textblob import TextBlob

def execute(arguments: dict):
    text = arguments.get("text")
    
    if not text:
        return "Sentiment error: No text provided"
    
    try:
        blob = TextBlob(text)
        
        # Get polarity (-1 to 1) and subjectivity (0 to 1)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment
        if polarity > 0.3:
            sentiment = "Positive 😊"
        elif polarity < -0.3:
            sentiment = "Negative 😞"
        else:
            sentiment = "Neutral 😐"
        
        # Confidence level
        confidence = abs(polarity)
        confidence_level = "High" if confidence > 0.6 else "Medium" if confidence > 0.3 else "Low"
        
        return (
            f"Text: {text}\n"
            f"Sentiment: {sentiment}\n"
            f"Polarity: {polarity:.2f} (-1 to 1)\n"
            f"Subjectivity: {subjectivity:.2f} (0 to 1)\n"
            f"Confidence: {confidence_level}"
        )
        
    except Exception as e:
        return f"Sentiment error: {e}"

if __name__ == "__main__":
    test_texts = [
        "I love this! It's absolutely amazing!",
        "This is terrible, I hate it.",
        "The weather is okay today.",
        "I'm feeling really happy about my new job!",
        "This product broke after one day. Very disappointed.",
    ]
    
    for text in test_texts:
        print(execute({"text": text}))
        print("-" * 40)