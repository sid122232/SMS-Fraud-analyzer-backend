from flask import Flask, request, jsonify

from phase2.threat_engine import analyze_msg

app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    message = data["message"]

    result = analyze_msg(message)

    print(message)
    print(result)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)