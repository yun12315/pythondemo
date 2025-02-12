# 全局列表，用于存储联系人
concats = []

def print_menu():
    print("-------------菜单-------------")
    print("1.添加联系人")
    print("2.删除联系人")
    print("3.修改联系人")
    print("4.查找联系人")
    print("5.显示所有联系人")
    print("6.退出通讯录")
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
        exit()
    else:
        print("无效的选择，请重新选择！")

def main():
    print_menu()
    while True:
        choice = input("请输入你的选择：")
        execute_choice(choice)

# 启动通讯录管理系统
main()