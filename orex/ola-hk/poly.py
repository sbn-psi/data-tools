def get_polynomial_func(coefficients):
    def polynomial(x):
        return sum(f * (x ** p) for (p,  f) in enumerate(coefficients))
    return polynomial

class Polynomials:
    def __init__(self, filename):
        self.funcs = {}
        with open(filename) as infile:
            for line in infile:
                tokens = line.split(",")
                name = tokens[0]
                coefficients = [float(x) for x in tokens[1:]]
                self.funcs[name] = get_polynomial_func(coefficients)

    def apply(self, key, value):
        return self.funcs[key](value)
