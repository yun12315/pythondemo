class Home:
    def __init__(self, address, area):
        self.address = address
        self.area = area
        self.free_area = area
        self.item_list = []
        print("创建了一个%s" % self.address)
        print("剩余%.2f" % self.free_area)
        print("家具有%s" % self.item_list)
        print("------------------------")
    def __str__(self):
        msg = "房间地址是%s,房间大小是%.2f,剩余大小是%.2f,家具有%s" % (self.address, self.area, self.free_area, self.item_list)
        msg += "当前房子里的物品有%s"%(str(self.item_list))
        return msg
    def add_item(self, item):
        print("要添加%s" % item)
        #self.free_area -= item.area

        self.free_area -= item.get_area()
        if item.area > self.free_area:
            print("无法添加%s" % item)
        else:
            #self.item_list.append(item.name)
            self.item_list.append(item.get_name())
            print("添加%s成功" % item)
            print("剩余%.2f" % self.free_area)
            print("家具有%s" % self.item_list)
            print("------------------------")
class Bed:
    def __init__(self, name, area):
        self.name = name
        self.area = area

    def __str__(self):
        return "家具是%s,大小是%.2f" % (self.name, self.area)

    def get_area(self):
        return self.area
    def get_name(self):
        return self.name


fangzi = Home("001", 120)
print(fangzi)
bed1 = Bed("席梦思", 4)
bed2 = Bed("大床", 5)
fangzi.add_item(bed2)
fangzi.add_item(bed1)
print(fangzi)