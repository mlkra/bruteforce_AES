import base64
import binascii
import sys
from itertools import product
from Crypto.Cipher import AES
from cryptography.hazmat.primitives import padding
from multiprocessing import Pool

missing_chars = 8

# key suffix
sufix = '8ffa112e989243f11f33067e9d85305900340fe8455694c720ab0302'

# initialization vector used to encrypt data
iv = binascii.unhexlify('0b91976b21829cdca28070daf27e0b3b')

# ciphertext to decipher
ciphertext = b'/oU3+lH1WI66pHDzbPSVFn6tboRhquR9L5PhYhXG9R7GGQ9pHIsYBqdjdKCEhkh7Sjf7RyH6T1CZD0CaudIOJi0G3JGwZlFFX4DGw35bkuZjK+Mr0hJ+GoP/1zMj7Q76w92wZGMXS0vGGzltVX0j5NpQYPeTNhh8M3ZQK4ajBANH7pv53UTfrZzr86XVj/rWME+bIjhH4xYkmYx76hJv5zdUmfX5HfEQ2Ylo+4Ac/hlABj4wDVRo4Lg64wvwmyryN8iyVQ+v4QXVn7cAakgFig=='

# for testing keys
def test_key(sufix, iv, ciphertext, symbol_list, start):
    mylist = product(symbol_list, repeat=missing_chars - 1)
    for prefix in mylist:
        try:
            prefix = ''.join(prefix)
            prefix = start + prefix
            key = binascii.unhexlify(prefix + sufix)
            aes = AES.new(key, AES.MODE_CBC, iv)
            msg = aes.decrypt(ciphertext)
            unpadder = padding.PKCS7(128).unpadder()
            msg = unpadder.update(msg) + unpadder.finalize()
            t = str(msg, "utf-8")
        except (UnicodeDecodeError, ValueError):
            pass
        else:
            #print(t)
            print(str(msg, "cp1252"))
            #break
            

ciphertext = base64.b64decode(ciphertext)

symbol_list = [chr(i) for i in range(48, 58)]
symbol_list.extend([chr(i) for i in range(65, 71)])

if __name__ == '__main__':
    parameters = [(sufix, iv, ciphertext, symbol_list, start) for start in symbol_list]
    with Pool() as p:
        p.starmap(test_key, parameters)
   
