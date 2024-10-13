
from db import get_column_data, get_members, get_columns
from security.encryption import decrypt

"""
● To add a new member to the system.

● To modify or update the information of a member in the system.

● To delete a member's record from the database (note that a consultant cannot delete a record but can only modify or update a member’s information).

● To search and retrieve the information of a member
"""

def modify_member():
    pass

def search_member(column, input):
    result_list = []
    data = get_members()
    columns = get_columns("members")
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

    return result_list

def see_members(member_list):
    decrypted_list = []
    for i in member_list:
        temp = []
        temp.append(i[0]) # id
        temp.append(decrypt(i[1])) # fn
        temp.append(decrypt(i[2])) # ln
        temp.append(i[3]) # age
        temp.append(i[4]) # gender
        temp.append(i[5]) # weight
        temp.append(decrypt(i[6])) # address
        temp.append(decrypt(i[7])) # email
        temp.append(decrypt(i[8])) # phone
        temp.append(i[9]) # registration_date
        decrypted_list.append(temp)

    return decrypted_list


def delete_member():
    pass