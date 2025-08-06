import sqlite3


def init_db():

    conn = sqlite3.connect("logs/predictions.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sepal_length REAL,
            sepal_width REAL,
            petal_length REAL,
            petal_width REAL,
            prediction TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def log_to_db(input_data, prediction):

    conn = sqlite3.connect("logs/predictions.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions (
            sepal_length, sepal_width, petal_length, petal_width, prediction
        ) VALUES (?, ?, ?, ?, ?)
    """, (
        input_data.sepal_length,
        input_data.sepal_width,
        input_data.petal_length,
        input_data.petal_width,
        str(prediction)
    ))
    conn.commit()
    conn.close()
