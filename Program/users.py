from db import get_users, verify_data, get_columns
from security.encryption import decrypt

def search_user(column, input):
    result_list = []
    data = get_users()
    columns = get_columns("users")
    c_index = 0
    for c in columns:
        if c == column:
            break
        c_index = c_index + 1

    if column != 'registration_date' and column != 'id':
        for d in data:
            temp_v = decrypt(d[c_index])
            if input in temp_v:
                result_list.append(d)

    else:
        for d in data:
            if input in str(d[c_index]):
                result_list.append(d)

def get_user_list():
    list_strings = []
    users = get_users()
    for i in users:
        temp = []
        temp.append(i[0])
        temp.append(decrypt(i[2]))
        temp.append(decrypt(i[4]))
        temp.append(decrypt(i[6]))
        temp.append(decrypt(i[7]))
        temp.append(i[8])
        list_strings.append(temp)

    return list_strings

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
