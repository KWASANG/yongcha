import sqlite3

def init_db():
    with sqlite3.connect("delivery.db") as con:
        cur = con.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS delivery_records (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            발송일 DATE,
            발송자 TEXT,
            차량번호 TEXT,
            목적지 TEXT,
            물품설명 TEXT,
            작성시간 TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        con.commit()

if __name__ == '__main__':
    init_db()
    print("데이터베이스가 초기화되었습니다.")
