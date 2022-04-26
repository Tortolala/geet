'''
[Module] Directory Scanner
'''
import os
import json
import hashlib


PATH = '/Users/tortolala/Desktop/dirtest/'


def list_files(path: str) -> list:

    files_to_ignore_raw = read_file_by_lines(path + '.geetignore')
    files_to_ignore = [file_name[:-1] for file_name in files_to_ignore_raw]
    all_files = os.listdir(path)
    files = []

    for file in all_files:
        if file not in files_to_ignore:
            files.append(file)

    return files


def read_file(path: str) -> str:

    with open(path, 'r') as reader:
        return reader.read()


def read_file_by_lines(path: str) -> list:

    with open(path, 'r') as reader:
        return reader.readlines()


def hash_file(path: str) -> str:

    file_text = read_file(path)
    file_hash = hashlib.sha1(file_text.encode('utf-8')).hexdigest()
    return file_hash


def get_hash_dict(path: str) -> dict:
    
    files = list_files(path)
    hash_collection = {}

    for file in files:
        hash_collection[file] = hash_file(path + file)
        
    return hash_collection


def save_hash_dict(path: str) -> None:

    with open(path + '.hashdict.json', 'w') as writer:
        hash_dict = get_hash_dict(path)
        json.dump(hash_dict, writer)

    return None


def read_current_hash_dict(path: str) -> dict:

    with open(path + '.hashdict.json', 'r') as reader:
        file = reader.read()
        return json.loads(file)


def scan_for_new_files(path: str) -> list:

    previous_files = read_current_hash_dict(path).keys()
    current_files = get_hash_dict(path).keys()
    new_files = []

    for file in current_files:
        if file not in previous_files:
            new_files.append(file)

    return new_files


def scan_for_deleted_files(path: str) -> list:
 
    previous_files = read_current_hash_dict(path).keys()
    current_files = get_hash_dict(path).keys()
    deleted_files = []

    for file in previous_files:
        if file not in current_files:
            deleted_files.append(file)

    return deleted_files


def scan_for_modified_files(path: str) -> list:

    previous_hash_dict = read_current_hash_dict(path)
    current_hash_dict = get_hash_dict(path)
    previous_files = previous_hash_dict.keys()
    current_files = current_hash_dict.keys()
    modified_files = []

    for file in current_files:
        if file in previous_files:
            if previous_hash_dict[file] != current_hash_dict[file]:
                modified_files.append(file)

    return modified_files
        

# print(list_files(PATH))
# print(read_file(PATH + 'main.py'))
# print(read_file_by_lines(PATH + 'main.py'))
# print(hash_file(PATH + 'main.py'))
# print(get_hash_dict(PATH))
# print(save_hash_dict(PATH))
# print(read_current_hash_dict(PATH))
print("New files:", scan_for_new_files(PATH))
print("Deleted files:", scan_for_deleted_files(PATH))
print("Modified files:", scan_for_modified_files(PATH))
