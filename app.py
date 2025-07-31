from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__) 
CORS(app)

# Replace with your actual Gemini API key
genai.configure(api_key="AIzaSyCOw7lRRgQ8tzJ65aoK6tKBZPj615Doov8")

model = genai.GenerativeModel("gemini-1.5-flash")

# Only allow questions related to these topics
ALLOWED_KEYWORDS = [
    "e-waste", "electronic waste", "recycling", "upcycling", "reuse",
    "sustainability", "climate change", "global warming",
    "carbon footprint", "environment", "pollution", "circular economy", "eco-friendly",
    "waste management", "green energy", "renewable energy", "camera", "smartwatch", "tv", "television", "mobile phone", "laptop", "computer", "tablet", "charger", "battery", "electronics", "microwave", "mouse", "keyboard", "printer", "speaker", "headphones", "air conditioner", "refrigerator", "washing machine", "dishwasher", "vacuum cleaner", "smart home devices", "smart appliances", "smart thermostat", "smart speaker", "smart light bulbs", "smart plugs", "smart cameras", "smart locks", "smart TVs", "smart displays", "smart wearables", "fitness tracker", "smartwatch accessories", "electronic accessories",
]

SYSTEM_PROMPT = (
    "You are AITANAbot, an expert AI assistant focused ONLY on sustainability, climate change, "
    "electronic waste, and the circular economy. Do NOT answer unrelated questions."
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])
    user_message = messages[-1]["content"].lower()

    # Keyword filtering
    if not any(keyword in user_message for keyword in ALLOWED_KEYWORDS):
        return jsonify({
            "response": "Sorry, I can only answer questions about sustainability, e-waste, climate change, and the circular economy. 🌱 Please ask something related to those topics."
        })

    # Add system prompt
    try:
        convo = model.start_chat(history=[
            {"role": "user", "parts": [SYSTEM_PROMPT]},
        ])

        response = convo.send_message(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
