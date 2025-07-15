import os
from multiprocessing import Pool, Manager

def copy_file(fileName, oldFolder_name, newFolder_name, queue):
    try: # 添加 try-except 块，处理文件操作可能出现的异常
        # 1.获取文件内容
        old_fr = open(os.path.join(oldFolder_name, fileName), "rb") # 使用 os.path.join 更安全
        content = old_fr.read()
        # 2.将文件内容写入到新的文件夹中
        new_fw = open(os.path.join(newFolder_name, fileName), "wb") # 使用 "wb" 以二进制写入，更通用
        new_fw.write(content)
        print(f"正在复制 {fileName}  进程ID: {os.getpid()}") # 打印进程ID，方便调试
        queue.put(fileName)  # 复制完成后放入队列
        old_fr.close()
        new_fw.close()
    except Exception as e: # 捕获更广泛的异常
        print(f"复制文件 {fileName} 出错: {e}")
        queue.put(None) # 放入 None 表示复制出错，主进程可以处理

def main():
    # 0.获取用户要copy的文件夹的名字
    oldFolder_name = input("请输入要copy的文件夹：")
    # 1.创建一个文件夹
    newFolder_name = oldFolder_name + "_副件"
    print("正在创建文件夹：", newFolder_name)
    try:
        os.mkdir(newFolder_name)
    except FileExistsError:
        print(f"文件夹 {newFolder_name} 已存在，将覆盖文件。")
    except Exception as e:
        print(f"创建文件夹 {newFolder_name} 出错: {e}")
        return  # 创建文件夹失败，直接退出

    # 2.获取old文件夹中的所有的文件名字
    try:
        fileNames = os.listdir(oldFolder_name)
    except FileNotFoundError:
        print(f"文件夹 {oldFolder_name} 不存在。")
        return
    except Exception as e:
        print(f"读取文件夹 {oldFolder_name} 文件列表出错: {e}")
        return

    # 3.使用多进程的方式copy原文件夹中的所有文件到新的文件夹中
    pool = Pool(5)
    queue = Manager().Queue()
    allNum = len(fileNames)
    print(f"总共 {allNum} 个文件需要复制...")
    for fileName in fileNames:
        pool.apply_async(func=copy_file, args=(fileName, oldFolder_name, newFolder_name, queue))

    num = 0
    print("正在复制...")
    while num < allNum:
        fileName_result = queue.get() # 只 get 一次
        if fileName_result is not None: # 检查是否复制成功 (如果 copy_file 中 put 了 None 表示出错)
            print(f"已完成复制: {fileName_result}")
            num += 1
            copyRate = num / allNum  # 计算进度
            print(f"copy进度：{copyRate * 100:.2f}%")
        else:
            print("复制过程中有文件出错，请查看错误信息。")
            num += 1 # 即使出错也计数，避免死循环
            copyRate = num / allNum
            print(f"copy进度：{copyRate * 100:.2f}% (包含错误)")


    print("copy成功")
    pool.close()
    pool.join()  # 等待所有的子进程执行完毕，再执行主进程


if __name__ == "__main__":
    main()