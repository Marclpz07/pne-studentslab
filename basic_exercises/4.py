

def rscore(score):
    result = ""
    if 9 <= score <= 10:
        result = "A"
    elif 7 <= score <= 8.9:
        result = "B"
    elif 5 <= score <= 6.9:
        result = "C"
    elif 3 <= score <= 4.9:
        result = "D"
    elif 0 <= score <= 2.9:
        result = "F"

    return result

print(rscore(9.5))