import pickle
from text_url import extract_url, analyze_url

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
SCAM_WORDS = {
    "won": 20,
    "winner": 20,
    "lottery": 30,
    "claim": 20,
    "click": 15,
    "urgent": 25,
    "reward": 20,
    "gift": 15,
    "verify": 25,
    "bank": 25,
    "otp": 30,
    "password": 30,
    "prize": 20,
    "free": 10,
    "limited": 15,
    "offer": 10
}

def analyze_msg(message):
    msg_vec = vectorizer.transform([message])
    sms_probability = float(model.predict_proba(msg_vec)[0][1])
    sms_score = float(sms_probability * 100)

    message_score = 0
    detected_words = []

    for word, risk in SCAM_WORDS.items():
      if word in message.lower():
        message_score += risk
        detected_words.append(word)

    urls = extract_url(message)
    url_results = []
    total_url_score = 0
    for url in urls :
      result = analyze_url(url)
      url_results.append(result)
      total_url_score += result["score"]

    # Final threat score 
    final_score = sms_score + total_url_score + message_score
    url_risks = [r["risk"] for r in url_results]

    if "Dangerous" in url_risks:
      risk = "Dangerous"

    elif "Suspicious" in url_risks and final_score >= 30:
     risk = "Suspicious"

    else:
     if final_score >= 90:
        risk = "Dangerous"

     elif final_score >= 45:
        risk = "Suspicious"

     else:
        risk = "Safe"
    if final_score >= 90:
        risk = "Dangerous"

    elif final_score >= 45:
        risk = "Suspicious"

    else:
        risk = "Safe"

    # FINAL OUTPUT
    

    return {

        "message": message,

        "sms_probability": round(sms_probability, 2),

        "sms_score": round(sms_score, 2),

        "urls_found": urls,

        "url_results": url_results,

        "total_url_score": total_url_score,

        "final_score": round(final_score, 2),

        "risk": risk, 
        "message_score": message_score,
        "detected_words": detected_words,
    }


if __name__ == "__main__":

    msg = input("Enter Message: ")

    result = analyze_msg(msg)

    print("\nFINAL RESULT:\n")

    print(result)