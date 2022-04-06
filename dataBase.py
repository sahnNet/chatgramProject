import sqlite3

DATABASE_NAME = 'userdata.db'
TABLE_NAME = 'Client'


def build_database():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''CREATE TABLE IF Not EXISTS {TABLE_NAME}
         (user_name text PRIMARY KEY,
          password text)
          ''')
    conn.commit()
    conn.close()


def creat_user(username, password):
    flag = True
    build_database()
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO {TABLE_NAME} VALUES (:user_name,:password)",
                       {'user_name': username, 'password': password})
    except:
        flag = False
    # cursor.execute(f"INSERT INTO {TABLE_NAME} VALUES (:user_name,:password)",
    #                {'user_name': username, 'password': password})
    conn.commit()
    conn.close()
    return flag


def is_exist(username, password):
    build_database()
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE user_name = '{username}' AND password = '{password}'")
    except:
        return None
    # cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE user_name = '{username}' AND password = '{password}'")
    user = cursor.fetchone()

    conn.commit()
    conn.close()

    return user
