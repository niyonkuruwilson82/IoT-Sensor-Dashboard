from flask import Flask, render_template, request, redirect
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow CORS if needed

def init_db():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                humidity REAL,
                temperature REAL,
                soil_moisture REAL,
                timestamp TEXT
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("SELECT humidity, temperature, soil_moisture, timestamp FROM sensor_data ORDER BY timestamp ASC")
        rows = c.fetchall()

    timestamps = [row[3] for row in rows]
    humidity = [row[0] for row in rows]
    temperature = [row[1] for row in rows]
    soil_moisture = [row[2] for row in rows]

    return render_template('index.html', timestamps=timestamps, humidity=humidity,
                           temperature=temperature, soil_moisture=soil_moisture)

@app.route('/submit', methods=['POST'])
def submit():
    humidity = float(request.form.get('humidity'))
    temperature = float(request.form.get('temperature'))
    soil_moisture = float(request.form.get('soil_moisture'))
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with sqlite3.connect("database.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO sensor_data (humidity, temperature, soil_moisture, timestamp) VALUES (?, ?, ?, ?)",
                  (humidity, temperature, soil_moisture, timestamp))
        conn.commit()

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)