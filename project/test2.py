class A():
    def __init__(self):
        self.att = ["a","d"]


class B():
    def __init__(self):
        self.att = list()

a = A()
b = B()

print(a.att)
print(b.att)

b.att = a.att

print(a.att)
print(b.att)

b.att.append("c")

print(a.att)
print(b.att)


tuple = ("integer[]","integer")

print(tuple)

