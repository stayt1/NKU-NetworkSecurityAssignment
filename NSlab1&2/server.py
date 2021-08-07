# tcp_server.py
'''服务器'''

from socket import *
from des import *
import rsa

HOST = ''  # 服务器主机地址
PORT = 23345  # 端口号
BUFSIZ = 2048  # 缓存区大小，单位是字节，这里设定了2K的缓冲区
DESKEY = "12345678"
ADDR = (HOST, PORT)  # 链接地址

tcpSerSock = socket(AF_INET, SOCK_STREAM)  # 创建一个TCP套接字
tcpSerSock.bind(ADDR)  # 绑定地址
tcpSerSock.listen(5)  # 最大连接数为5

while True:  # 无限循环
    print("Waiting to be connected...")
    tcpCliSock, addr = tcpSerSock.accept()  # 等待接受连接
    print("Got Connection from Client ", addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)  # 接收数据,BUFSIZ是缓存区大小
        enstrData = data.decode("utf-8")
        strData = desdecode(enstrData,DESKEY) # 对收到的数据进行解密
        if strData == 'quit':
            break

        print("Receive Message From", addr, ": "+strData)

        msg = input("Reply:")
        msg = msg
        enmsg = desencode(msg, DESKEY) # 对发送的消息进行加密
        # 对要发送的数据进行编码
        tcpCliSock.send(enmsg.encode("utf-8"))
        # 如果服务器端输入的是q，则停止对话并且退出程序
        if msg == 'quit':
            break

    tcpCliSock.close()  # 关闭连接

tcpSerSock.close()  # 关闭服务器