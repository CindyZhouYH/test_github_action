import where

py_url = where.first("python3")
py_prefix = "python3"
print(py_url)
if py_url is None:
    py_url = where.first("python")
    py_prefix = "python"
    print(py_url)
    if py_url is None:
        raise WindowsError
