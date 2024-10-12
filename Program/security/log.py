import db
from db import create_connection, get_exact_data_from_column, hash_data, get_logs, verify_data
from security.encryption import encrypt, decrypt
from datetime import datetime

def log_activity(username, activity, suspicious):

    conn = create_connection()
    cursor = conn.cursor()
    current_datetime = datetime.now()
    date = current_datetime.strftime('%Y-%m-%d')  # Format as YYYY-MM-DD
    time = current_datetime.strftime('%H:%M:%S')
    seen = '0'
    suspicious = '1' if suspicious else '0'
    cursor.execute('INSERT INTO logs (date, time, seen, username, activity, suspicious) VALUES (?, ?, ?, ?, ?, ?)',
                   (encrypt(date),
                    encrypt(time),
                    hash_data(seen),
                    encrypt(username),
                    encrypt(activity),
                    hash_data(suspicious)))
    conn.commit()
    conn.close()

# when admin logs in do this check - call function after login
# when suspicious log (1) + not seen (0) - return TRUE + LOGS
# display notification with option to view log - in display

def check_unseen_sus_logs():
    data = get_exact_data_from_column('logs', 'suspicious', 'seen', '1', '0')
    return data

def set_seen_all_logs():
    seen = '1'
    e_seen = hash_data(seen)
    print(e_seen)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE logs SET seen = ?", (e_seen,))
    conn.commit()
    conn.close()

def see_logs(logs):
    list_strings = []
    for i in logs:
        temp = []
        temp.append(i[0])           # id
        temp.append(decrypt(i[1]))  # date
        temp.append(decrypt(i[2]))  # time
        temp.append('not seen') if verify_data(i[3], '0') else temp.append('seen')  # seen
        temp.append(decrypt(i[4]))  # username
        temp.append(decrypt(i[5]))  # activity
        temp.append('not suspicious') if verify_data(i[6], '0') else temp.append('suspicious')  # suspicious
        list_strings.append(temp)
    return list_strings


