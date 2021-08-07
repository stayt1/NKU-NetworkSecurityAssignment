from socket import *
from time import ctime
import select
import rsa
import des
from stdio import stdio

judgeFlag = False

HOST = ''
PORT = 12346
BUFSIZE = 1024
ADDR = (HOST, PORT)

tcpServer = socket(AF_INET, SOCK_STREAM)
tcpServer.bind(ADDR)
tcpServer.listen(5)
# gets = [tcpServer, sys.stdin]
gets=[tcpServer,stdio.STDIN_FILENO]

while True:
    print("Waiting for connection...")
    tcpClient, addr = tcpServer.accept()
    print("Got Connection from Client:", addr)
    gets.append(tcpClient)
    rsaPubKey, rsaPriKey = rsa.generateKeyPair()
    # print(rsaPubKey)
    # print(rsaPriKey)
    tcpClient.send(str(rsaPubKey[0]).encode("utf-8"))
    tcpClient.send(str(rsaPubKey[1]).encode("utf-8"))

    keyLen=tcpClient.recv(BUFSIZE)
    keyLen=int(keyLen.decode("utf-8"))
    encryDESKEY=[]
    for i in range(0,keyLen):
        encryDESKEYData=tcpClient.recv(BUFSIZE)
        encryDESKEY.append(int(encryDESKEYData.decode("utf-8")))

    # print(encryDESKEY)
    DESKEY = rsa.decrypt(rsaPriKey,encryDESKEY)

    flag = "Exchange Key Successfully! Begin to Chat..."
    print(flag)
    enFlag=des.desencode(flag,DESKEY)
    enFlagData = enFlag.encode("utf-8")
    tcpClient.send(enFlagData)

    while True:
        readyInput, readyOutput, readyException = select.select(gets, [], [])
        for indata in readyInput:
            if indata == tcpClient:
                data = tcpClient.recv(BUFSIZE)
                enstrData=data.decode("utf-8")
                strData = des.desdecode(enstrData,DESKEY)
                # if not data:
                #     break
                if strData == 'quit':
                    # tcpClient.close()
                    judgeFlag = True
                    print("The client quit the chat!")
                    break
                print('[%s]' % (ctime()), addr, ":"+strData)
                # print('[%s]: %s' % (ctime(), data.decode('utf-8')))
            else:
                # msg = input()
                msg = stdio.read()
                msg = msg.decode("utf-8")
                msg = msg.replace("\n","")
                # print("we have input from server:", msg)
                # msg = msg

                # if not data:
                #     break
                #tcpClient.send(bytes(data, 'utf-8'))
                enMsg = des.desencode(msg, DESKEY)
                tcpClient.send(enMsg.encode("utf-8"))
                if msg == 'quit':
                    # tcpClient.close()
                    judgeFlag = True
                    # print("closing one discussing client")
                    break
        if judgeFlag:
            break
    gets.remove(tcpClient)
    tcpClient.close()
    judgeFlag = False
    # print("client closed!")

tcpServer.close()
