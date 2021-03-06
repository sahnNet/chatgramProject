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
    build_database()
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(f"INSERT INTO {TABLE_NAME} VALUES (:user_name,:password)",
                       {'user_name': username, 'password': password})
        conn.commit()
        conn.close()
        return is_exist(username=username, password=password)
    except:
        return None


def is_exist(username, password):
    build_database()
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT rowid,* FROM {TABLE_NAME} WHERE user_name = '{username}' AND password = '{password}'")
        user = cursor.fetchone()

        conn.commit()
        conn.close()

        return user[0]
    except:
        return None
