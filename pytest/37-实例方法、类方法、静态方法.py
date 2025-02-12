class Game(object):
    """游戏类"""
    # 类属性
    count = 0
    # 实例方法
    def __init__(self,name):
        self.name = name
        print("初始化游戏"+self.name)

    # 类方法
    @classmethod
    def start(cls):
        cls.count = 100
        print("开始游戏")
    @classmethod
    def end(cls):
        print("结束游戏")

    def print_menu(self):
        const = input("请输入游戏名称：")
        print("===========================")
        print(const+"的游戏菜单")
        print("1.开始游戏")
        print("2.结束游戏")
        print("3.退出游戏")
        choice = int(input("请输入你的选择："))
        Game.execute_choice(choice)
        return choice

    # 静态方法
    @staticmethod
    def execute_choice(choice):
        for i in range(3):
            if choice == 1:
                print("开始游戏")
            elif choice == 2:
                print("结束游戏")
            elif choice == 3:
                exit()
            else:
                print("无效的选择，请重新选择！")
#game = Game("python")
#Game.start() #
#game.start() #
#print(Game.count)
Game.print_menu("")