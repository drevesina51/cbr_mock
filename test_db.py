import sqlite3

def test_db():
    with sqlite3.connect("currency.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM requests")
        print("Last 5 requests:")
        for row in cursor.fetchall()[-5:]:
            print(row)

if __name__ == "__main__":
    test_db()