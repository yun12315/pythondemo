import sys
#sys.getrefcount()

class T:
    pass

t1=T()
t2=t1
del t2
del t1 
print(sys.getrefcount(t1))