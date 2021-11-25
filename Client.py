import socket
import sys
import threading
import DES
import rsa
import time
import os
import key_gen

def read_msg(sock):
    while True:
        data = sock.recv(65535)
        if len(data) == 0:
            break
        data = data.decode("utf-8")
        if len(data.split(',')) == 3:
            user, msg , enc_key= data.split(',')

            print("\n\n-----Receiving Message-----")
            print("\nMessage before decrypted: " + DES.bin2hex(msg))
            msg_key = rsa.decrypt(d, N, enc_key)
            key_rev = msg_key.split()[::-1]
            print("After decrypted:")
            msg = DES.encrypt(msg, key_rev)
            print("(" + user + ")" + " : " + DES.bin2ascii(msg))
            print("\nInput username destination : ")
        else:
            print("\n"+data)
            



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 6666))
sock.send(bytes(sys.argv[1], "utf-8"))

thread_cli = threading.Thread(target=read_msg, args=(sock,))
thread_cli.start()

key = key_gen.randStr(N=8) #des key


e, d, N = rsa.genereateKeys(5)
keypath = os.getcwd() + '/key/'
if not os.path.exists(keypath):
    os.mkdir(os.getcwd() + '/key/')
key_folder = os.listdir(keypath)
f = open(keypath+sys.argv[1]+'.txt', 'w+')
f.write(str(e)+" "+str(N))
f.close()



rkb = []
DES.init_keys(key, rkb)

while True:
    key_folder = os.listdir(keypath)
    dest = input("Input username destination : ")
    if dest+'.txt' not in key_folder:
        print(dest + ' is not on client list')
    else :
        f = open(keypath+dest+'.txt', 'r')
        recv_e, recv_N= f.read().split()
        enc_key = rsa.encrypt(int(recv_e), int(recv_N), ' '.join(map(str, rkb)))
        msg = input("Input message :")
        if len(msg) != 8:
            print("Message must be 8 characters long")
        else:
            msg = DES.ascii2bin(msg)
            cipher_text = DES.encrypt(msg, rkb)
            print("Encrypted message: " + DES.bin2hex(cipher_text))
            sock.send(bytes("{}|{}|{}".format(dest, cipher_text, enc_key), "utf-8"))
        time.sleep(0.5)
