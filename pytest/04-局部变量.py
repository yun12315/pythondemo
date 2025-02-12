# 局部变量a = 300

g_a = 300
def test1():
    global g_a
    g_a = 100
    print("a=%d"%g_a)
    return g_a
def test2():
    #a = test1()
    print("a=%d"%g_a)

test1()
test2()