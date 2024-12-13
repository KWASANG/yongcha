from flask import Flask, request, render_template, send_file
import sqlite3
import pandas as pd
from io import BytesIO

# 초기화 실행
if __name__ == '__main__':
    init_db()
    app.run()

app = Flask(__name__)

# 데이터베이스 초기화 함수
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

# 홈 화면
@app.route('/')
def index():
    return render_template('index.html')

# 데이터 저장
@app.route('/save', methods=['POST'])
def save_data():
    data = request.form
    with sqlite3.connect("delivery.db") as con:
        cur = con.cursor()
        cur.execute('''
        INSERT INTO delivery_records (발송일, 발송자, 차량번호, 목적지, 물품설명)
        VALUES (?, ?, ?, ?, ?)
        ''', (data['발송일'], data['발송자'], data['차량번호'], data['목적지'], data['물품설명']))
        con.commit()
    return "<script>alert('저장되었습니다!'); window.location='/';</script>"

# 데이터 조회
@app.route('/records', methods=['GET'])
def view_records():
    with sqlite3.connect("delivery.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM delivery_records")
        rows = cur.fetchall()
    return render_template('records.html', rows=rows)

# 데이터 다운로드
@app.route('/export', methods=['GET'])
def export_data():
    with sqlite3.connect("delivery.db") as con:
        df = pd.read_sql_query("SELECT * FROM delivery_records", con)
        output = BytesIO()
        df.to_csv(output, index=False, encoding='utf-8-sig')
        output.seek(0)
    return send_file(output, mimetype='text/csv', as_attachment=True, download_name='delivery_records.csv')

# 특정 기록 수정 페이지
@app.route('/edit/<int:record_id>', methods=['GET', 'POST'])
def edit_record(record_id):
    with sqlite3.connect("delivery.db") as con:
        cur = con.cursor()
        if request.method == 'POST':
            data = request.form
            cur.execute('''
            UPDATE delivery_records
            SET 발송일 = ?, 발송자 = ?, 차량번호 = ?, 목적지 = ?, 물품설명 = ?
            WHERE ID = ?
            ''', (data['발송일'], data['발송자'], data['차량번호'], data['목적지'], data['물품설명'], record_id))
            con.commit()
            return "<script>alert('수정되었습니다!'); window.location='/records';</script>"
        else:
            cur.execute("SELECT * FROM delivery_records WHERE ID = ?", (record_id,))
            record = cur.fetchone()
    return render_template('edit.html', record=record)


# 초기화 실행
if __name__ == '__main__':
    init_db()
    app.run()
