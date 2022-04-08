def register_message(username, password):
    return f"Make -Option <user:{username}> -Option <pass:{password}>"


def login_message(username, password):
    return f"Connect -Option <user:{username}> -Option <pass:{password}>"


def group_message(username):
    return f"Group -Option <user:{username}>"


def gm_message(username, msg):
    return f"GM -Option <from:{username}> -Option <message_len:{len(msg)}> -Option <message_body:{msg}>"


def pm_message(from_user, to_user, msg):
    return f"PM -Option <from:{from_user}> -Option <to:{to_user}> -Option <message_len:{len(msg)}> -Option <message_body:{msg}>"


def list_users_message(username):
    return f"Users -Option <user:{username}>"


def exit_chatroom_message(username):
    return f"End -Option <user:{username}>"
