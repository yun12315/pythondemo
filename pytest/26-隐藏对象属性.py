class Dog:
    def set_age(self, age):
        if age>0 and age<=100:
            self.age = age
        else:
            print('年龄不合法')

    def get_age(self):
        return self.age

dog = Dog()
dog.age =-10
dog.name ="小白"
print(dog.name+"的年龄是"+str(dog.age))
dog.set_age(10)
age = dog.get_age()
print(age)