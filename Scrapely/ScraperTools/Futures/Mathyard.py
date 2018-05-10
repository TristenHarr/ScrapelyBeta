import math
class CDF:

    def __init__(self, var: list):
        self.var = var

    def __eq__(self, other):
        if isinstance(other, CDF):
            if len(self) == len(other):
                return all([self[o] == other[o] for o in range(len(other))])
        return False

    def __getitem__(self, item):
        return self.var[item]

    def __len__(self):
        return len(self.var)

    def __str__(self):
        return str(self.var)

    def inc(self, n):
        out = list(self.var)
        out[n] += 1
        return CDF(out)

    def get_inc(self):
        out = []
        for e in range(len(self)):
            k = self.inc(e)
            if k not in out:
                out.append(k)
        return out

    @staticmethod
    def get_list_inc(input: list):
        out = []
        for e in input:
            for f in e.get_inc():
                if f not in out:
                    out.append(f)
        return out


# l = 12
#
# for P in range(1, l):
#     a = [CDF([0 for k in range(P)])]
#     print(len(a), end="\t")
#     for N in range(l-1):
#         a = CDF.get_list_inc(a)
#         print(len(a), end="\t")
#     print()

def get_combinations(N, P):
    n = N + P - 1
    k = P - 1
    return (math.factorial(n))/(math.factorial(k)*math.factorial(n-k))
print(get_combinations(10000, 5))