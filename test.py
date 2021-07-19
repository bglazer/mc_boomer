class A():
    def x(self, y):
        return y+3

class B(A):
    def z(self, q):
        return q+41

b = B()

print(b.x(41))
