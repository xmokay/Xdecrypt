import os
import sys
import argparse
import base64
import configparser
import ctypes
import getpass
from ctypes import wintypes

from win32api import GetComputerName, GetUserName
from win32security import LookupAccountName, ConvertSidToStringSid
from Crypto.Hash import SHA256
from Crypto.Cipher import ARC4
def get_config_file_dir():
    global args
    if args.dir:
        return args.dir
    else:
        # get documents dir
        buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
        # NetSarang Computer dir
        ns_dir = os.path.join(buf.value, r"NetSarang Computer")
        return ns_dir

def get_master_password_list():
    global args
    lst = []
    if args.master:
        lst.append(args.master)
    if args.sid:
        lst.append(args.sid)
    # 7
    tmp = GetUserName()[::-1] + ConvertSidToStringSid(LookupAccountName(GetComputerName(), GetUserName())[0])
    lst.append(tmp[::-1])
    # 6
    lst.append(GetUserName() + ConvertSidToStringSid(LookupAccountName(GetComputerName(), GetUserName())[0]))
    return lst

def decrypt_string(a1, a2):
    v1 = base64.b64decode(a2)
    v3 = ARC4.new(SHA256.new(a1.encode('ascii')).digest()).decrypt(v1[:len(v1) - 0x20])
    if SHA256.new(v3).digest() == v1[-32:]:
        return v3.decode('ascii')
    else:
        return None

def try_decrypt_string(password, master_password_lst):
    global args
    for master_password in master_password_lst:
        r = decrypt_string(master_password, password)
        if r:
            return r
    if not args.master:
        args.master = getpass.getpass("Enter master password: ")
        master_password_lst.insert(0, args.master)
        r = decrypt_string(args.master, password)
        if r:
            return r
    return None


def main():
    global args
    parser = argparse.ArgumentParser(description="xsh, xfp password decrypt")
    parser.add_argument("-d", "--dir", default="", type=str, help="The directory where the .xsh file is stored")
    parser.add_argument("-s", "--sid", default="", type=str, help="`username`+`sid`, user `whoami /user` in command.")
    parser.add_argument("-p", "--password", default="", type=str, help="the encrypted password to decrypt.")
    parser.add_argument("-m", "--master", default="", type=str, help="master password")
    args = parser.parse_args()

    master_password_lst = get_master_password_list()
    if args.password:
        dec = try_decrypt_string(args.password, master_password_lst)
        if dec:
            print(dec)
            sys.exit(0)
        else:
            print("decryption failed")
            sys.exit(1)

    ns_dir = get_config_file_dir()
    for root, dirs, files in os.walk(ns_dir):
        for f in files:
            if f.endswith(".xsh") or f.endswith(".xfp"):
                filepath = os.path.join(root, f)
                cfg = configparser.ConfigParser()
                try:
                    cfg.read(filepath)
                except UnicodeDecodeError:
                    cfg.read(filepath, encoding="utf-16")

                try:
                    if f.endswith(".xsh"):
                        host = "{}:{}".format(cfg["CONNECTION"]["Host"], cfg["CONNECTION"]["Port"])
                        username = cfg["CONNECTION:AUTHENTICATION"]["UserName"]
                        password = try_decrypt_string(cfg["CONNECTION:AUTHENTICATION"]["Password"], master_password_lst)
                    else:
                        host = "{}:{}".format(cfg["Connection"]["Host"], cfg["Connection"]["Port"])
                        username = cfg["Connection"]["UserName"]
                        password = try_decrypt_string(cfg["Connection"]["Password"], master_password_lst)
                    print(
                        f"{filepath:=^100}\nHost:     {host}\nUsername: {username}\nPassword: {password}")
                except Exception as e:
                    print(f"{filepath:=^100}\nError:{e}")

if __name__ == "__main__":
    main()