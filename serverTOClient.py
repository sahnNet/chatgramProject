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


def message(msg):
    return f"Message -Option {msg}"
