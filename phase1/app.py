from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    msg = data["message"]
    
    vec = vectorizer.transform([msg])
    prob = model.predict_proba(vec)[0][1]

    if prob > 0.5:
        result = "spam"
    elif prob > 0.3:
        result = "suspecious"
    else:
        result = "Safe"
    return jsonify({
        "result" : result,
        "probability": round(float(prob), 2)
    })
app.run(host="0.0.0.0" , port= 5000)