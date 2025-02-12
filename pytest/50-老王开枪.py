class Person(object):
    """人"""
    def __init__(self, name, gun):
        """
        初始化方法
        :param name: 老王的名字
        :param gun: 老王的枪
        """
        super(Person, self).__init__()
        self.name = name
        self.gun = None
        self.hp = 100

    def add_bullet(self,danjia,bullet):
        """
        给枪装子弹
        :param danjia: 弹夹
        :param bullet: 子弹
        :return:
        """
        danjia.add_bullet(bullet)
        print("子弹装填完毕")

    def add_danjia(self,gun,danjia):
        """
        给枪装弹夹
        :param gun: 老王枪
        :param danjia: 弹夹
        :return:
        """
        gun.add_danjia(danjia)
        print("弹夹装填完毕")

    def take_gun(self,gun):
        """
        老王拿枪
        :param gun: 老王拿枪
        :return:
        """
        self.gun = gun
        print("老王 already has a gun")

    def __str__(self):
        if self.gun:
            return "%s的血量为：%d,枪的信息为:%s"%(self.name,self.hp,self.gun)
        else:
            if self.hp <= 0:
                return "%s already dead"%self.name
            else:
                return "%s的血量为：%d,他没有枪"%(self.name,self.hp)

    def kou_ban_ji(self,enemy):
        """
        老王开枪
        :param enemy: 老王开枪打敌人
        :return:
        """
        self.gun.fire(enemy)
    def diaoxue(self,sha_shang_li):
        """
        掉血
        :param sha_shang_li: 子弹威力
        :return:
        """
        self.hp -= sha_shang_li
class Gun(object):
    """枪"""
    def __init__(self,name):
        super(Gun,self).__init__()
        self.name = name # 枪的名字
        self.danjia = None # 弹夹引用

    def add_danjia(self,danjia):
        self.danjia = danjia
        print("枪 already has a danjia")

    def __str__(self):
        if self.danjia:
            return "枪的信息为：%s,弹夹的信息为：%s"%(self.name,self.danjia)
        else:
            return "枪的信息为：%s,弹夹的信息为：%s"%(self.name,None)

    def fire(self,enemy):
        """
        开枪
        :param enemy: 老王开枪打敌人
        :return:
        """
        zidan_temp = self.danjia.tanchu_zidan()
        if zidan_temp:
            zidan_temp.dazhong(enemy)
            print("%s正在打%s"%(self.name,enemy.name))
            enemy.hp -= 10
            print("%s的血量是%d"%(enemy.name,enemy.hp))
        else:
            print("老王已经没有子弹了")

class Enemy(object):
    """敌人"""
    def __init__(self, name):
        super(Enemy, self).__init__()
        self.name = name

class Bullet(object):
    """子弹"""
    def __init__(self,arg):
        super(Bullet,self).__init__()
        self.count = 0
        self.count += 1
        self.sha_shang_li = arg
        print("子弹已经发射了%d发"%self.count)
        print("发射子弹")
    def dazhong(self,enemy):
        """
        子弹打敌人
        :param enemy: 老王开枪打敌人
        :return:
        """
        #敌人掉血（一颗子弹的威力)
        enemy.diaoxue(self.sha_shang_li)
        print("子弹打到了%s"%enemy.name)
class Danjia(object):
    """弹夹"""
    def __init__(self,max_bullet):
        super(Danjia,self).__init__()
        self.max_bullet = max_bullet # 弹夹中子弹的数量
        self.bullet_list = [] # 子弹列表

    def add_bullet(self,bullet):
        self.bullet_list.append(bullet)
        self.max_bullet -= 1
        print("子弹已经发射了%d发"%self.max_bullet)

    def __str__(self):
        return "弹夹的信息为：%d/%d"%(len(self.bullet_list),self.max_bullet)

    def tanchu_zidan(self):
        """
        弹出子弹
        :return:
        """
        if self.bullet_list:
            return self.bullet_list.pop()
        else:
            print("老王没有子弹了")
def main():
    """用来控制整个程序的流程"""
    #1. 创建老王对象
    wang = Person('老王', 'ak47')

    #2. 创建一个枪对象
    ak47 = Gun('ak47')

    #3. 创建一个弹夹对象
    danjia = Danjia(20)

    #4. 创建子弹对象
    for i in range(20):
        bullet = Bullet(1)
        #5. 老王给枪装子弹
        wang.add_bullet(danjia,bullet)

    #6. 老王给枪装弹夹
    wang.add_danjia(ak47,danjia)
    print(danjia)

    #7. 老王拿枪
    wang.take_gun(ak47)
    print(wang)
    #8. 创建一个敌人
    laosong = Person('小明', 'AK47')
    print(laosong)
    #9. 老王开枪
    for i in range(30):
        wang.kou_ban_ji(laosong)
        print(laosong)

if __name__ == '__main__':
    main()