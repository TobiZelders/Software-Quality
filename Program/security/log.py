from db import create_connection, get_data_from_table

def log_activity(username, activity, suspicious):

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO logs (date, time, seen, username, activity, suspicious) VALUES (DATE(), TIME(), ?, ?, ?, ?)',
                   (0, username, activity, 1 if suspicious else 0))
    conn.commit()
    conn.close()

# when admin logs in do this check - call function after login
# when suspicious log (1) + not seen (0) - return TRUE + LOGS
# display notification with option to view log - in display

def alert_admin_sus_log():
    data = get_data_from_table('logs')
