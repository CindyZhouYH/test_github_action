from dcmodule import execute_dcmodule

if __name__ == "__main__":
    _success, _message, _data = execute_dcmodule(
        "not_exist.py",
        stdin = "",
        stdout = "",
    )
    print(_success)
    print(_message)
    print(_data)
