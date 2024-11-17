# database.py
import sqlite3

class WordMapper:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_random_word_of_length(self, n):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = f"""
        SELECT cet4_word
        FROM cet4_word
        WHERE LENGTH(cet4_word) = {n}
        ORDER BY RANDOM()
        LIMIT 1
        """

        cursor.execute(query)
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        return result[0] if result else None

    def find_word(self, word):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        query = f"""
        SELECT *
        FROM cet4_word
        WHERE cet4_word = '{word}'
        """

        cursor.execute(query)
        result = cursor.fetchone()
        # print(result)
        
        cursor.close()
        conn.close()

        return {
            "id": result[0],
            "word": result[1],
            "pronunciation": result[2],
            "meaning": result[3],
            "distotion": result[4],
            "phase": result[5],
            "example": result[6]
        } if result else None

if __name__ == "__main__":
    mapper = WordMapper("./cet4_words.db")
    print(mapper.find_word("hello"))