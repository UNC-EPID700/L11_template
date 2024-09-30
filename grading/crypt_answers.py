import argparse
import os
from cryptography.fernet import Fernet
import requests


def get_key(key: bytes) -> Fernet: 
    return Fernet(key=key)

def encrypt(filepath: str, key: str, outpath: str) -> bool: 
    if not os.path.exists(path=key): 
        raise Exception("key path does not exist")
    if not os.path.exists(path=filepath): 
        raise Exception("filepath path does not exist")
    
    with open(key, "rb+") as f: 
        k = f.read()
        
    fkey = get_key(k)

    with open(filepath, "rb+") as f: 
        filebytes = f.read()

    encrypted = fkey.encrypt(filebytes)

    os.makedirs(name=os.path.split(p=outpath)[0], exist_ok=True)

    with open(f"{outpath}_encrypted", "wb+") as f: 
        f.write(encrypted)

    return True

def decrypt(encryptedpath: str, key: str):
    assert requests.head(encryptedpath).status_code == 200, f"Answer key path does not exist; this is autograder issue."
        
    fkey = get_key(str.encode(key))

    decrypted = fkey.decrypt(token=str.encode(requests.get(url=encryptedpath).text))

    return decrypted
    

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description="Encrypt a file.")
    parser.add_argument('input_file', type=str, help='The file to Encrypt')
    parser.add_argument('key_file', type=str, help='The key file')
    parser.add_argument('output_file', type=str, help='The destination file for the Encrypted content')

    args = parser.parse_args()

    encrypt(args.input_file, args.key_file, args.output_file)