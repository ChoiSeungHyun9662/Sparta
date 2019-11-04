def is_Prime(num):
    is_prime = True
    for i in range(2, num):
        module = num % i
        if module == 0:
            is_prime = False
    return is_prime

print(is_Prime(8))
print(is_Prime(11))
print(is_Prime(113))