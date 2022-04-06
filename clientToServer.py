def register_message(username, password):
    return f"Make -Option <user:{username}> -Option <pass:{password}>"


def login_message(username, password):
    return f"Connect -Option <user:{username}> -Option <pass:{password}>"
