
"""
Custom format for map data saving
"""

file_id = b"SVDT"
type_name = ".savedata"

#writer
def write_file(filename: str, content: bytes, dim: tuple[int, int]):
    filename_full = filename + type_name
    with open(filename_full, "wb") as file:
        file.write(file_id + bytes(dim) + content)
        file.close()

#reader
def read_file(filename: str) -> tuple[tuple[int, int],  bytes]:
    with open(filename, "rb") as file:
        magic_check = file.read(4)
        dd = (0, 0)
        payload = b""
        if magic_check == file_id:
            dd = tuple(file.read(2))
            payload = file.read()
        else:
            print("error reading file")
        file.close()
        return dd, payload

#checker
def istype(filename: str):
    if type_name in filename:
        with open(filename, "rb") as file:
            magic_check = file.read(4)
            file.close()
            return magic_check == file_id

