from db import create_connection

def log_activity(username, activity, suspicious):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (date, time, username, activity, suspicious) VALUES (DATE(), TIME(), ?, ?, ?)',
                   (username, activity, 1 if suspicious else 0))
    conn.commit()
    conn.close()
