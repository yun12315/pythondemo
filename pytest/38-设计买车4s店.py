class CarStore(object):
    def __init__(self):
        self.factory = CarFactory()
    def order(self,car_type):
        return self.factory.select_car_type(car_type)
class CarFactory(object):
    def select_car_type(self,car_type):
        if car_type == '索纳塔':
            return Sonata()
        elif car_type == '君威':
            return Kona()

class Car(object):
    def move(self):
        print('车在移动')
    def stop(self):
        print('车在停止')

class Sonata(Car):
    def move(self):
        print(' soi na ta 在加速')
class Kona(Car):
    def move(self):
        print(' k on a 在加速')

car_store = CarStore()
car = car_store.order('君威')
car.move()