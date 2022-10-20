class Lehmer:

    def __init__(self, multiplier, start, modulus):
        self.a = multiplier
        self.R = start
        self.m = modulus
        self.x = self.R

    def GetNext(self):
        self.x = self.a * self.x % self.m
        return self.x / self.m
