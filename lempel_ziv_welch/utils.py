def read_file(file_path: str):
    with open(file_path, 'rb') as f:
        data = f.read()
    return data


def write_file(file_path: str, extension: str, data: bytes):
    with open(f"{file_path}.{extension}", 'wb') as f:
        f.write(data)
