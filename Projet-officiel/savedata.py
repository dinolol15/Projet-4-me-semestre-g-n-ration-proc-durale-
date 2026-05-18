
"""
Custom format for map data saving
"""

file_id = b"SVDT"
type_name = ".savedata"

#writer
def write_file(filename: str, content: bytes):
    filename_full = filename + type_name
    with open(filename_full, "wb") as file:
        file.write(file_id + content)
        file.close()

#reader
def read_file(filename: str) -> bytes:
    with open(filename, "rb") as file:
        magic_check = file.read(4)
        payload = b""
        if magic_check == file_id:
            payload = file.read()
        else:
            print("error reading file")
        file.close()
        return payload

#checker
def istype(filename: str):
    if type_name in filename:
        with open(filename, "rb") as file:
            magic_check = file.read(4)
            file.close()
            return magic_check == file_id

