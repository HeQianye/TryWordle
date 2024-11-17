# main.py
from flask import Flask, request, jsonify
from mapper import WordMapper

app = Flask(__name__)

# 连接到 SQLite 数据库
db_path = './cet4_words.db'
word_mapper = WordMapper(db_path)

@app.route('/get_word', methods=['GET'])
def get_word():
    n = request.args.get('length', type=int)
    if n is None:
        return jsonify({"error": "Please provide a valid length"}), 400

    word = word_mapper.get_random_word_of_length(n)
    if word:
        return jsonify({"word": word})
    else:
        return jsonify({"error": f"No word found with length {n}"}), 404

@app.route('/find_word', methods=['POST'])
def find_word():
    data = request.get_json()
    word = data.get('word')
    if word is None:
        return jsonify({"error": "Please provide a word"}), 400

    found_word = word_mapper.find_word(word)
    if found_word:
        return jsonify({"word": found_word})
    else:
        return jsonify({"error": f"Not Found"}), 404

if __name__ == '__main__':
    app.run(debug=True)