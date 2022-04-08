def register_message(id):
    result = "User Not Accepted -Option "
    if id is not None:
        result = f"User Accepted -Option <id:{id}>"
    return result


def login_message(id):
    result = "ERROR -Option"
    if id is not None:
        result = f"Connected -Option <id:{id}>"
    return result


def gm_message(username, msg):
    return f"GM -Option <from:{username}> -Option <message_len:{len(msg)}> -Option <message_body:{msg}>"


def pm_message(from_user, to_user, msg):
    return f"PM -Option <from:{from_user}> -Option <to:{to_user}> -Option <message_len:{len(msg)}> -Option <message_body:{msg}>"


def list_users_message(msg):
    return f"USERS -Option USERS_LIST:\n{msg}"
