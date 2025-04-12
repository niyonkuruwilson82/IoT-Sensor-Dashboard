from flask import Flask, render_template, request, redirect
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

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
        # Fetch all data for chart
        c.execute("SELECT humidity, temperature, soil_moisture, timestamp FROM sensor_data ORDER BY timestamp ASC")
        all_rows = c.fetchall()

        # Fetch recent 10 entries for table
        c.execute("SELECT humidity, temperature, soil_moisture, timestamp FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
        table_rows = c.fetchall()

    # Separate values for chart
    timestamps = [row[3] for row in all_rows]
    humidity = [row[0] for row in all_rows]
    temperature = [row[1] for row in all_rows]
    soil_moisture = [row[2] for row in all_rows]

    return render_template(
        'index.html',
        timestamps=timestamps,
        humidity=humidity,
        temperature=temperature,
        soil_moisture=soil_moisture,
        table_data=table_rows
    )

@app.route('/submit', methods=['POST'])
def submit():
    try:
        humidity = float(request.form.get('humidity'))
        temperature = float(request.form.get('temperature'))
        soil_moisture = float(request.form.get('soil_moisture'))
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect("database.db") as conn:
            c = conn.cursor()
            c.execute("INSERT INTO sensor_data (humidity, temperature, soil_moisture, timestamp) VALUES (?, ?, ?, ?)",
                      (humidity, temperature, soil_moisture, timestamp))
            conn.commit()
    except Exception as e:
        print("Error inserting data:", e)

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True ,host="0.0.0.0", port=5000)