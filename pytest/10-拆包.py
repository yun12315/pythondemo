def unpack_list(list_data,*args,**kwargs):
    """
    拆包
    :param list_data:
    :return:
    """
    a, b, c = list_data
    return a, b, c
def unpack_dict(**kwargs):
    """
    拆包
    :param kwargs:
    :return:
    """
    print(kwargs)

aa = (1,2,3)
bb = {'a':1,'b':2,'c':3}
print(unpack_list((22,33,44),*aa,**bb))