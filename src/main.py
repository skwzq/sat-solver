from sys import argv

from solver import Solver


with open(argv[1], 'r') as file:
    input_ = file.read()

input_ = input_.split()

n_vars = int(input_[2])

f = [[]]

for i in range(4, len(input_)-1): # the last number is always 0
    literal = int(input_[i])
    if literal == 0:
        f.append([])
    else:
        f[-1].append(literal)


sat = Solver(f, n_vars).solve()

print(sat)
