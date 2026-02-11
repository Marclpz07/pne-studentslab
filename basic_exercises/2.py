text = "  Hello, World! Welcome to Python Programming.  "


a = text.strip()
b = text.split()
c = len(b)



print(a)
print(c)
print(text.title())
print(text.startswith("Hello"))
print(text.endswith("ing"))
print(text.find("Python"))
print("-".join(b))