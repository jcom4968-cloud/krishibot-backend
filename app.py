from flask import Flask, request, jsonify
from flask_cors import CORS
import openai, os

app = Flask(__name__)
CORS(app)

# OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Krishi Bot API is running ✅"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("q", "")
        if not question:
            return jsonify({"answer": "No question provided"}), 400

        # OpenAI 0.28 compatible Completion API
        completion = openai.Completion.create(
            engine="gpt-3.5-turbo",  # 0.28 version uses engine instead of model
            prompt=f"তুমি একজন কৃষি বিশেষজ্ঞ। সহজ ভাষায় কৃষি ও চাষাবাদ সম্পর্কিত পরামর্শ দাও।\nUser: {question}\nBot:",
            max_tokens=300,
            temperature=0.3
        )

        answer = completion.choices[0].text.strip()
        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"answer": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
