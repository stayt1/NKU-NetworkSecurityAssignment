# tcp_client.py
'''客户端'''

from socket import *
from des import *
import random
import rsa
import select

def generatDESKEY(n):
    pool="abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+-={}"
    key=[]
    for i in range(n):
        key.append(random.choice(pool))
        keys=''.join(key)
    return keys

print('Please input the server address:')
HOST = input() # 输入服务器端主机号
PORT = 23345  # 端口号
BUFSIZ = 2048  # 缓存区大小，单位是字节，这里设定了2K的缓冲区
DESKEY = "12345678"
# DESKEY = generatDESKEY(8)

ADDR = (HOST, PORT)  # 链接地址

tcpCliSock = socket(AF_INET, SOCK_STREAM)  # 创建一个TCP套接字
# tcpCliSock.bind(ADDR) #绑定地址
tcpCliSock.connect(ADDR)  # 绑定地址
print('Connect Successful! Begin to Chat...')



while True:
    msg = input('Client:')  # 输入数据
    msg = msg
    enmsg = desencode(msg, DESKEY) # 对发送的消息进行加密
    tcpCliSock.send(enmsg.encode("utf-8"))

    # 如果客户端输入的是q，则停止对话并且退出程序
    if msg == 'quit':
        break

    data = tcpCliSock.recv(BUFSIZ)  # 接收数据,BUFSIZ是缓存区大小
    enstrData = data.decode("utf-8")
    strData = desdecode(enstrData,DESKEY) # 对收到的消息进行解密
    print("Server:"+strData)
    # 判断服务器端是否发送q，是就退出此次对话
    if strData == 'quit':
        break

tcpCliSock.close()