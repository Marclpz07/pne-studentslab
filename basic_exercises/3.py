from textwrap import shorten

temperatures = [15.5, 17.2, 14.8, 16.0, 18.3, 20.1, 19.5]


print(temperatures[2])
print(max(temperatures))
print(min(temperatures))


def mean_value(lst):
    new_value = 0
    for x in lst:
        new_value = new_value + x

    return round((new_value / len(lst)), 1)

print(mean_value(temperatures))

count = 0
for i in temperatures:
    if i > 17:
        count += 1

print(count)

ordered = sorted(temperatures)
print( ordered)