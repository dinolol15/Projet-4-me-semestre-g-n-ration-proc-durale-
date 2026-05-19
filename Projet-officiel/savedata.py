
"""
Custom format for map data saving
"""

FILE_ID = b"SVDT"
TYPE_NAME = ".savedata"

#writer
def write_file(filename: str, content: bytes, dim: tuple[int, int]):
    """Writer for the file
    1. 'SVDT' in binary (4 bytes)
    2. Map size (max 255x255) (2 bytes)
    3. Binary payload
    """
    filename_full = filename + TYPE_NAME
    with open(filename_full, "wb") as file:
        file.write(FILE_ID + bytes(dim) + content)
        file.close()

#reader
def read_file(filename: str) -> tuple[tuple[int, int],  bytes]:
    """Reader, checks if right file type
    if yes returns map size + payload"""
    with open(filename, "rb") as file:
        magic_check = file.read(4)
        dd = (0, 0)
        payload = b""
        if magic_check == FILE_ID:
            dd = tuple(file.read(2))
            payload = file.read()
        else:
            print("error reading file")
        file.close()
        return dd, payload

#checker
def istype(filename: str) -> bool:
    """Checks if the file type is .savedata"""
    if TYPE_NAME in filename:
        with open(filename, "rb") as file:
            magic_check = file.read(4)
            file.close()
            return magic_check == FILE_ID
    return False
