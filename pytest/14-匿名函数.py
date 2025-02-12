nums = [5,23,54,67,243,853,1]
nums.sort()
nums.sort(reverse=True)
print(nums)

infors = [{'name':'zhangsan','age':20},{'name':'wangwu','age':40},{'name':'lisi','age':30}]
infors.sort(key=lambda x:x['age'])
print(infors)