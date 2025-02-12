def line_conf(a,b):
    def line(x):
        return a*x+b
    return line
line = line_conf(4,2)
print(line(3))