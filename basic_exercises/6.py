def is_even_number(n):
    if n % 2 == 0:
        result = True
    else:
        result = False
    return result

print(is_even_number(4))
print(is_even_number(7))
print(is_even_number(0))
print(is_even_number(-3))

def classify_triangle(a, b, c):
    if a == b == c:
        res = "equilateral"
    elif a != b != c:
        res = "scalane"
    else:
        res = "isosceles"

    return res

print(classify_triangle(5, 5, 5))
print(classify_triangle(3, 3, 4))
print(classify_triangle(3, 4, 5))