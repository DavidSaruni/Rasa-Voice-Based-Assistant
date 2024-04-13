import tempfile
import os
from uuid import uuid4


TMP_FOLDER_NAME = "voice_assistant_tmp" 


def create_if_does_not_exist(path:str):
    if not os.path.exists(path):
        os.makedirs(path)

def get_tmp_folder_path():
    path = tempfile.gettempdir()
    path = os.path.join(path, TMP_FOLDER_NAME)
    create_if_does_not_exist(path)
    return path


def get_unique_file_path()-> str:
    file_path = os.path.join(get_tmp_folder_path(), str(uuid4()))
    return file_path

def create_unique_tmp_file(file_suffix:str)-> str:
    file_path = f"{get_unique_file_path()}_{file_suffix}"
    return file_path

def persist_binary_file_locally(data:bytes, file_suffix: str)-> str:
    file_path = create_unique_tmp_file(file_suffix=file_suffix)
    with open(file_path, "wb") as f:
        f.write(data)
    return file_path


if __name__ == "__main__":
    print("get_tmp_folder_path() >>",get_tmp_folder_path())