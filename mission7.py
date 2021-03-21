class ComplexNumber:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __add__(self, other):
        return f'the sum is equal: {self.a + other.a} + {self.b + other.b} * i'

    def __mul__(self, other):
        return f'product equals: {self.a * other.a - (self.b * other.b)} + {self.b * other.a} * i'


c_1 = ComplexNumber(4, -8)
c_2 = ComplexNumber(6, 11)
print(c_1 + c_2)
print(c_1 * c_2)
