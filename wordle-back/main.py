from flask import Flask, request, jsonify
from flask_cors import CORS
from mapper import WordMapper

app = Flask(__name__)
CORS(app)  # 允许所有域名访问

# 连接到 SQLite 数据库
db_path = './cet4_words.db'
word_mapper = WordMapper(db_path)

def make_response(success, status_code, message, data=None):
    return jsonify({
        "status_code": status_code,
        "success": success,
        "message": message,
        "data": data
    }), status_code

@app.route('/get_word', methods=['GET'])
def get_word():
    n = request.args.get('length', type=int)
    print(n)
    if n is None:
        return make_response(False, 200, "Please provide a valid length")

    word = word_mapper.get_random_word_of_length(n)
    if word:
        print(word)
        return make_response(True, 200, "Word retrieved successfully", {"word": word})
    else:
        return make_response(False, 200, f"No word found with length {n}")

@app.route('/find_word', methods=['POST'])
def find_word():
    data = request.get_json()
    word = data.get('word')
    if word is None:
        return make_response(False, 200, "Please provide a word")

    found_word = word_mapper.find_word(word)
    if found_word:
        return make_response(True, 200, "Word found successfully", {"word": found_word})
    else:
        return make_response(False, 200, "Not Found")

if __name__ == '__main__':
    app.run(debug=True)