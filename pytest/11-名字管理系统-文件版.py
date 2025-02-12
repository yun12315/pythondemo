# 全局列表，用于存储联系人
concats = []

def print_menu():
    print("-------------菜单-------------")
    print("1.添加联系人")
    print("2.删除联系人")
    print("3.修改联系人")
    print("4.查找联系人")
    print("5.显示所有联系人")
    print("6.保存")
    print("7.加载已保存数据")
    print("8.退出通讯录")
    print("------------------------------")

def add_contact():
    "添加联系人"
    name = input("请输入联系人姓名：")
    phone = input("请输入联系人电话：")
    contact = [name, phone]
    concats.append(contact)
    #concats.extend(contact)
    print("联系人添加成功！")

def modify_contact():
    "修改联系人"
    name = input("请输入要修改的联系人姓名：")
    for i, contact in enumerate(concats):
        if contact[0] == name:
            new_name = input("请输入新的姓名：")
            new_phone = input("请输入新的电话：")
            concats[i] = [new_name, new_phone]
            print("联系人修改成功！")
            return
    else:
        print("未找到该联系人！")

def delete_contact():
    "删除联系人"
    name = input("请输入要删除的联系人姓名：")
    for i, contact in enumerate(concats):
        if contact[0] == name:
            concats.pop(i)
            print("联系人删除成功！")
            return
    else:
        print("未找到联系人")


def show_all_contact():
    "显示所有联系人"
    if not concats:
        print("通讯录为空！")
    else:
        print("显示所有联系人:")
        for contact in concats:
            print(f"姓名: {contact[0]}, 电话: {contact[1]}")

def search_contact():
    "查找联系人"
    name = input("请输入要查找的联系人姓名：")
    # 创建一个标志，用于检查是否找到联系人
    found = False
    for contact in concats:
        if contact[0] == name:
            print(f"姓名: {contact[0]}, 电话: {contact[1]}")
            #found = True
            break
    else:
        print("未找到该联系人！")
    # 如果遍历完整个通讯录没有找到联系人
    #if not found:
    #    print("未找到该联系人！")

def save_2_file():
    "保存通讯录到文件"
    with open("contacts.txt", "w") as f:
        f.write(str(concats))
        print("通讯录保存成功！")
        f.close()
def load_from_file():
    "从文件加载通讯录"
    global concats
    try:
        with open('contacts.txt', 'r', encoding='gbk') as f:
            # print(f"文件已打开，文件名为：{f.name}")
            # for line in f:
            #     line = line.strip()
            #     if not line:  # 跳过空行
            #         continue
            #     parts = line.split(",")
            #     if len(parts) == 2:
            #         name, phone = parts
            #         print(name, phone)
            #     else:
            #         print(f"警告: 行 '{line}' 格式不正确，跳过")
            concats = eval(f.read())
            print("通讯录加载成功！"+str(concats))
            f.close()
    except FileNotFoundError:
        print("文件未找到")
    except Exception as e:
        print(f"发生错误: {e}")


def execute_choice(choice):
    if choice == "1":
        add_contact()
    elif choice == "2":
        delete_contact()
    elif choice == "3":
        modify_contact()
    elif choice == "4":
        search_contact()
    elif choice == "5":
        show_all_contact()
    elif choice == "6":
        save_2_file()
    elif choice == "7":
        load_from_file()
    elif choice == "8":
        exit()
    else:
        print("无效的选择，请重新选择！")

def main():
    print("欢迎使用通讯录管理系统！")
    load_from_file()
    print_menu()
    while True:
        choice = input("请输入你的选择：")
        execute_choice(choice)

# 启动通讯录管理系统
main()