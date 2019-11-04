# Print
#print('hello world!')

#list
# a_list = list()
# print(a_list)
# a_list.append(1)
# print(a_list)
# a_list.append([2,3])
# print(a_list)
# print(a_list[1][1])

def allsum(mylist):
    sum = 0
    for i in mylist:
        sum += i
    return sum

ten_list = range(10)
print(allsum(ten_list))