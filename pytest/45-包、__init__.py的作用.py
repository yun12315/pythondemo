# __init__.py 作用定义文件夹是否为包
def recvmsg(sock, size):
    """
    接收消息
    :param sock:
    :param size:
    :return:
    """
    msg = b''
    while len(msg) < size:
        data = sock.recv(size - len(msg))
        if not data:
            return None
        msg += data
    return msg