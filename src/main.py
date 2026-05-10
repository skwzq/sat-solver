from sys import argv

from parse_files import parse_cnf
from solver import solve_sat


cnf, n_vars = parse_cnf(argv[1])

solution = solve_sat(cnf, n_vars)

if solution:
    print(' '.join(str(x) for x in solution))
else:
    print('unsatisfiable')
