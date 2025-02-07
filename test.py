import math

def rootList():
    lst = []
    for i in range(1, 5):
        user_input = int(input("Enter a number: "))
        lst.append(user_input)

    root_lst = [math.sqrt(i) for i in lst]
    print(root_lst)
    return root_lst

a = rootList()