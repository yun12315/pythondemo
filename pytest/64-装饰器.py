def makeBold(fn):
    """
    makeBold(fn)
    """
    print("-----正在装饰1--------")
    print(fn)
    def wrapped():
        print("-----1----")
        return "<b>" + fn()+"</b>"
    return wrapped
def makeItalic(fn):
    """
    makeItalic(fn)
    """
    print("-----正在装饰2--------")
    print(fn)
    def wrapped():
        print("-----2----")
        return "<i>" + fn()+"</i>"
    return wrapped
@makeBold # hello = makeBold(hello)
@makeItalic # hello = makeItalic(hello)
def hello():
    print("-----3----")
    return "hello world"

ret = hello()
print(ret)
