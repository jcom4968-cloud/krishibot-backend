from flask import Flask, request, jsonify
import openai, os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Krishi Bot API is running ✅"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("q", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "তুমি একজন কৃষি বিশেষজ্ঞ। সহজ ভাষায় কৃষি ও চাষাবাদ সম্পর্কিত পরামর্শ দাও।"},
            {"role": "user", "content": question}
        ],
        temperature=0.3,
        max_tokens=300
    )

    answer = completion.choices[0].message["content"]
    return jsonify({"answer": answer})
