my_cards = [{"name":"杨春鱼","age":18,"sex":"女"},{"name":"李白","age":100,"sex":"男"},
{"name":"小白","age":38,"sex":"男"}]
find_name = input("请输入您要查找的姓名：")

for nums in my_cards:
    name = nums['name']
    if name == find_name:
        print("找到了此人，姓名："+name+"，年龄："+str(nums['age'])+"，性别:"+nums['sex'])
        break
else:
    print("查无此人！")