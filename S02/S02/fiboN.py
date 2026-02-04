
def fibon(n):
    a = 0
    b = 1
    i = 1
    while i < n:
        c = a + b
        a = b
        b = c
        i += 1
    return c




print("5th term is:",fibon(5))
print("5th term is:",fibon(10))
print("5th term is:",fibon(15))