from flask import Flask, request, jsonify
from flask_cors import CORS
import openai, os

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

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "তুমি একজন কৃষি বিশেষজ্ঞ। সহজ ভাষায় কৃষি ও চাষাবাদ সম্পর্কিত পরামর্শ দাও।"},
                {"role": "user", "content": question}
            ],
            temperature=0.3,
            max_tokens=300
        )

        answer = completion.choices[0].message["content"].strip()
        return jsonify({"answer": answer})

    except Exception as e:
        print("Error:", e)  # Debug log
        return jsonify({"answer": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
