#1.获取要重命名的文件夹名字
import os

folder_name = input("请输入要重命名的文件夹：")
# 2.获取指定文件夹中的所有文件名
file_names = os.listdir((folder_name))
#os.chdir(folder_name)
# 3.重命名
# 5.遍历所有文件名
for file_name in file_names:
    # 3.拼接出旧文件名和新文件名
    old_file_name = folder_name + '/' + file_name
    new_file_name = folder_name + '/' + file_name.replace('text', 'test')
    print(old_file_name, new_file_name)
    # 4.重命名文件
    os.rename(old_file_name, new_file_name)