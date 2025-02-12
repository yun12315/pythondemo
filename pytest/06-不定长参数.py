def sum_2_nums(a, b,c=33,*args,**kwargs):
    print(a)
    print(b)
    print(c)
    print(args)
    print(kwargs)
    return a + b
    for i in args:
        result += i
    print("result=%d"%result)

sum_2_nums(1,2,3,4,task=5,done=6)