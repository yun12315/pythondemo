class SweetPotato:
    def __init__(self):
        self.cooked_level = 0
        self.cooked_string = "生的"
        self.condiments = []
    def __str__(self):
        return "地瓜状态：%s, 烤制程度：%d,添加的作料有:%s" % (self.cooked_string, self.cooked_level,str(self.condiments))
    def cook(self, time):
        self.cooked_level += time
        if self.cooked_level >= 0 and  self.cooked_level < 3:
            self.cooked_string = "生的"
        elif self.cooked_level >= 3 and self.cooked_level < 5:
            self.cooked_string = "半生不熟"
        elif self.cooked_level >= 5:
            self.cooked_string = "熟的"
        elif self.cooked_level >= 6:
            self.cookedString = "烤好了"
            print("地瓜已经烤熟了，不能再烤了")
    def add_condiments(self, condiment):
        self.condiments.append(condiment)
        print("添加调料%s成功！" % condiment)


di_gua = SweetPotato()
print(di_gua)
di_gua.cook(1)
print(di_gua)
di_gua.cook(1)
print(di_gua)
di_gua.cook(1)
print(di_gua)
di_gua.cook(1)
print(di_gua)
di_gua.cook(1)
print(di_gua)
di_gua.cook(1)
print(di_gua)

sweet_potao = SweetPotato()
sweet_potao.add_condiments("辣子")
sweet_potao.add_condiments("香菜")
sweet_potao.cook(6)
print(sweet_potao)