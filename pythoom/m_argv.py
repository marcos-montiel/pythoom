import globals


def m_check_parm(check: str) -> bool:
    for i in range(1, globals.my_argc):
        if check.lower() == globals.my_argv[i].lower():
            return True
    return False
