from Crypto.Cipher import DES
from Crypto.Hash import SHA256
from getpass import getpass
from Crypto.Protocol.KDF import PBKDF2
import mimetypes


Key_length = 100005
salt = "$ez*&214097GDAKACNASC;LSOSSBAdjskasnmosuf!@#$^()_adsa"
# Encrypting function
def encryptor(path, passw1):
    try:
        with open(path, 'rb') as file:
            data = file.read()

        # Padding
        while len(data) % 8 != 0:
            data += b" "

        # Hashing original data with SHA256
        hash_of_original = SHA256.new(data=data)
        # Salting and hashing password
        key_enc = PBKDF2(passw1, salt, 48, Key_length)
        # Encrypting using triple 3-key DES
        print("Wait, it is being encrypted...\n")
        try:
            cipher1 = DES.new(key_enc[0:8], DES.MODE_CBC, key_enc[24:32])
            ciphertext1 = cipher1.encrypt(data)
            cipher2 = DES.new(key_enc[8:16], DES.MODE_CBC, key_enc[32:40])
            ciphertext2 = cipher2.decrypt(ciphertext1)
            cipher3 = DES.new(key_enc[16:24], DES.MODE_CBC, key_enc[40:48])
            ciphertext3 = cipher3.encrypt(ciphertext2)

            print('------ENCRYPTION SUCCESSFUL-------')
        except:
            print('Encryption failed. Possible causes: Library not installed properly, low device memory, incorrect padding, or conversions.')
            exit()
        # Adding hash at the end of encrypted bytes
        ciphertext3 += hash_of_original.digest()
        # Saving the file encrypted
        encrypted_file_path = "encrypted_temp_file_to_encrypt"
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(ciphertext3)

        return encrypted_file_path
    except Exception as e:
        print(f"Error during encryption: {str(e)}")
        exit()

   


# Decrypting function
def decryptor(encrypted_file_path, passw1):
    try:
        with open(encrypted_file_path, 'rb') as encrypted_file:
            encrypted_data_with_hash = encrypted_file.read()

    except:
        print(f"Unable to read source cipher data. Make sure the file {encrypted_file_path} is in the same directory. Exiting...")
        exit()

    # Extracting hash and cipher data without hash
    extracted_hash = encrypted_data_with_hash[-32:]
    encrypted_data = encrypted_data_with_hash[:-32]

    # Salting and hashing password
    key_dec = PBKDF2(passw1, salt, 48, Key_length)

    # Decrypting using triple 3-key DES
    print("Decrypting...")
    try:
        cipher1 = DES.new(key_dec[16:24], DES.MODE_CBC, key_dec[40:48])
        plaintext1 = cipher1.decrypt(encrypted_data)
        cipher2 = DES.new(key_dec[8:16], DES.MODE_CBC, key_dec[32:40])
        plaintext2 = cipher2.encrypt(plaintext1)
        cipher3 = DES.new(key_dec[0:8], DES.MODE_CBC, key_dec[24:32])
        plaintext3 = cipher3.decrypt(plaintext2)

    except:
        print("Decryption failed. Possible causes: Library not installed properly, low device memory, incorrect padding, or conversions.")

    # Hashing decrypted plaintext
    hash_of_decrypted = SHA256.new(data=plaintext3)

    # Matching hashes
    if hash_of_decrypted.digest() == extracted_hash:
        print("Password Correct!")
        print("------DECRYPTION SUCCESSFUL------")
    else:
        print("Incorrect Password!")
        exit()

    # Saving the decrypted file
    try:
        epath = encrypted_file_path
        if epath[:10] == "encrypted_":
            epath = epath[10:]
        decrypted_file_path = "decrypted_" + epath
        with open(decrypted_file_path, 'wb') as file:
            file.write(plaintext3)
        print(f"File saved successfully with name {decrypted_file_path}")
        return decrypted_file_path
    except:
        print("Failed to save decrypted file! Exiting...")
        exit()




           