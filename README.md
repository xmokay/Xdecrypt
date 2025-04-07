# Xdecrypt

Xshell Xftp password decrypt

## Setup
```
pip3 install -r requirements.txt
```

## Usage
```
usage: Xdecrypt.py [-h] [-d DIR] [-s SID] [-p PASSWORD] [-m MASTER]

xsh, xfp password decrypt

options:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     The directory where the .xsh file is stored
  -s SID, --sid SID     `username`+`sid`, user `whoami /user` in command.
  -p PASSWORD, --password PASSWORD
                        the encrypted password to decrypt.
  -m MASTER, --master MASTER
                        master password
```

```
$ python3 Xdecrypt.py
Enter master password: xxxxxxxx
================D:\Documents\NetSarang Computer\7\Xshell\Sessions\test.xsh=================
Host:     172.0.0.1:22
Username: root
Password: 123
```

```
$ python3 Xdecrypt.py -d "D:\Documents\NetSarang Computer"
Enter master password: xxxxxxxx
================D:\Documents\NetSarang Computer\7\Xshell\Sessions\test.xsh=================
Host:     172.0.0.1:22
Username: root
Password: 123
```

```
$ python3 Xdecrypt.py -m your_master_password
================D:\Documents\NetSarang Computer\7\Xshell\Sessions\test.xsh=================
Host:     172.0.0.1:22
Username: root
Password: 123
```

```
$python Xdecrypt.py -p "BztDpmWkWSBCL51Bfkhn79xPuKBKHz//H6B+mY6G9/eieuM="
Enter master password: xxxxxxxx
123
```

```
$ whoami /user
用户信息
----------------

用户名               SID
==================== =============================================
computername\username sid

$ python3 Xdecrypt.py
=============C:\Users\yourname\Documents\NetSarang Computer\6\Xftp\Sessions\192.168.1.2.xfp=============
Host:     192.168.1.2:22
Username: root
Password: test
==========C:\Users\d2x3\Documents\NetSarang Computer\6\Xshell\Sessions\192.168.1.2.xsh===========
Host:     192.168.1.2:22
Username: root
Password: test
========C:\Users\d2x3\Documents\NetSarang Computer\6\Xshell\Sessions\test\192.168.1.2.xsh========
Host:     192.168.1.2:22
Username: root
Password: test

$ python3 Xdecrypt.py -s username+sid -p "D:\somewhere\NetSarang Computer"
=============D:\somewhere\NetSarang Computer\6\Xftp\Sessions\192.168.1.2.xfp=============
Host:     192.168.1.2:22
Username: root
Password: test
==========D:\somewhere\NetSarang Computer\6\Xshell\Sessions\192.168.1.2.xsh===========
Host:     192.168.1.2:22
Username: root
Password: test
========D:\somewhere\NetSarang Computer\6\Xshell\Sessions\test\192.168.1.2.xsh========
Host:     192.168.1.2:22
Username: root
Password: test

$ python Xdecrypt.py -s username+sid -p password
test
```