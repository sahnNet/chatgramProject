def register_message(flag):
    result = "User Not Accepted -Option "
    if flag:
        result = "User Accepted -Option "
    return result


def login_message(flag):
    result = "ERROR -Option"
    if flag is not None:
        result = f"Connected -Option <id:{flag}>"
    return result
