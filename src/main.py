from sys import argv

from parse_files import parse_cnf
from solver import Solver


f, n_vars = parse_cnf(argv[1])

solution = Solver(f, n_vars).solve()

if solution:
    print(' '.join(str(x) for x in solution))
else:
    print('unsatisfiable')
