#1 获取用户要复制的文件名
old_file_name = input("请输入要复制的文件名:")
#2 打开要复制的文件
old_file = open(old_file_name, "rb")
#3 创建一个新文件
new_file = open(old_file_name + ".bak", "wb")
#4 从旧文件中读取数据，并且写入到新文件中
while True:
    content = old_file.read(1024)
    if content:
        new_file.write(content)
    else:
        break
#5 关闭文件
old_file.close()
new_file.close()