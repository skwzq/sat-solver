from sys import argv

from solver import Solver


with open(argv[1], 'r') as file:
    input_ = file.read()

input_ = input_.splitlines()

i = 0
while i < len(input_):
    if input_[i][0] == 'p':
        break
    i += 1

n_vars = int(input_[i].split()[2])

f = []

for j in range(i+1, len(input_)):
    clause = [int(x) for x in input_[j].split()[:-1]]
    f.append(clause)


solution = Solver(f, n_vars).solve()

if solution:
    for x in solution:
        print(str(x) + ' ')
else:
    print('unsatisfiable')
