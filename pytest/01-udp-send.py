from socket import *

#创建udp套接字
udpSocket = socket(AF_INET,SOCK_DGRAM)
udpSocket.bind(("",57673))
recvData = udpSocket.recvfrom(1024) #接收数据 1024为接收数据的最大字节数
print(recvData) #udp tcp socket都是接收数据，udp没有返回数据，tcp有返回数据 都是全双工的
#udpSocket.sendto(b"hello world,i miss you",("192.168.0.133",8080))
#udpSocket.sendto(b"do you remember me ,i miss you",("192.168.0.133",8080))

