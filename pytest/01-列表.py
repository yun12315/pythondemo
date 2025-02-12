nums = [5,23,54,67,243,853,1]
nums.append(100)
nums.extend([100,100])
print(nums[0])
print(nums)
print(nums[1:-2:3])
#nums.pop()
#del nums[0]
nums.remove(5)
print(nums)
# for i in nums:
#     print(i)

infors = [{'name':'zhangsan','age':20},{'name':'wangwu','age':40}]
for i in infors:
    print(i)
    #print(i['name'])