from socket import *
from time import ctime
import select
import des
import rsa
import random
import sys
from stdio import stdio

def generatDESKEY(n):
    pool="abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-={}"
    key=[]
    for i in range(n):
        key.append(random.choice(pool))
        keys=''.join(key)
    return keys

judgeFlag = False

HOST = 'localhost'
PORT = 12346
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpClient = socket(AF_INET, SOCK_STREAM)
tcpClient.connect(ADDR)
# gets = [tcpClient, sys.stdin]
gets = [tcpClient,stdio.STDIN_FILENO]
print('Connect Successful!')

rsaPubKey=[]
rsaPubKey.append(int(tcpClient.recv(BUFSIZE).decode("utf-8")))
rsaPubKey.append(int(tcpClient.recv(BUFSIZE).decode("utf-8")))
# print(rsaPubKey)
DESKEY = generatDESKEY(8)
encryDESKEY = rsa.encryption(rsaPubKey, DESKEY)
# print(encryDESKEY)
tcpClient.send(str(len(encryDESKEY)).encode("utf-8"))
for i in range(0,len(encryDESKEY)):
    # print(str(encryDESKEY[i]))
    tcpClient.send(str(encryDESKEY[i]).encode("utf-8"))

while True:
    readyInput, readyOutput, readyException = select.select(gets, [], [])
    for indata in readyInput:
        if indata == tcpClient:
            data = tcpClient.recv(BUFSIZE)
            enstrData=data.decode("utf-8")
            strData = des.desdecode(enstrData, DESKEY)
            print('[%s]' % (ctime()), "Server: " + strData)
            if strData == 'quit':
                # tcpClient.close()
                print("The server quit the chat!")
                judgeFlag = True
                break
        else:
            msg = stdio.read()
            msg = msg.decode("utf-8")
            msg = msg.replace("\n","")
            # print("we have input from client:",msg)
            enMsg = des.desencode(msg, DESKEY)
            tcpClient.send(enMsg.encode("utf-8"))
            if msg == 'quit':
                # print("we close")
                judgeFlag = True
                break
    if judgeFlag:
        break
tcpClient.close()
judgeFlag = False
# print("we close")
sys.exit(0)
# exit(0)
