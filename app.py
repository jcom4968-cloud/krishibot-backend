from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # Mobile app থেকে access করার জন্য

# OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Krishi Bot API is running ✅"

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debug log
        question = data.get("q", "")
        if not question:
            return jsonify({"answer": "No question provided"}), 400

        # OpenAI 0.28.0 interface অনুযায়ী
        completion = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=f"তুমি একজন কৃষি বিশেষজ্ঞ। সহজ ভাষায় কৃষি ও চাষাবাদ সম্পর্কিত পরামর্শ দাও।\n\nUser: {question}\nBot:",
            temperature=0.3,
            max_tokens=300
        )

        answer = completion.choices[0].text.strip()
        print("Bot response:", answer)  # Debug log
        return jsonify({"answer": answer})

    except Exception as e:
        print("Error:", e)  # Debug log
        return jsonify({"answer": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    # Render এর জন্য host=0.0.0.0 এবং port environment variable ব্যবহার
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
