import unittest

from parse_files import parse_cnf, parse_sol
from solver import solve_sat

class TestSolver(unittest.TestCase):
    def test_solve_sat_returns_empty_if_empty_formula(self):
        self.assertEqual(solve_sat(cnf=[], n_vars=0), [])

    def test_solve_returns_none_if_unsatisfiable(self):
        self.assertEqual(solve_sat(cnf=[[1, -2], [-1], [2]], n_vars=2), None)

    def test_solve_returns_correct_truth_assignment_2_variables(self):
        self.assertEqual(solve_sat(cnf=[[1, -2], [2]], n_vars=2), [1, 2])

    def test_solve_returns_correct_truth_assignment_4_variables_and_bigger_clauses(self):
        self.assertEqual(solve_sat(cnf=[[-1, -2, 3, 4], [2, 3], [1, -2], [1, -3], [-3, 4], [-2, -4]], n_vars=4), [1, -2, 3, 4])

    def test_solve_returns_correct_truth_assignment_multiple_backjumps(self):
        self.assertEqual(solve_sat(cnf=[[-1, 2], [-2, 3], [-2, 4], [-3, -4], [-3, 4], [-4, 5], [-4, 6], [-5, -6], [6]], n_vars=6), [-1, -2, -3, -4, -5, 6])

    # the files used in the following tests are from https://github.com/arminbiere/cadical/tree/master/test/cnf

    def test_solve_returns_correct_truth_assignment_sqrt2809(self):
        cnf, n_vars = parse_cnf('src/tests/sqrt2809.cnf')
        self.assertEqual(solve_sat(cnf, n_vars), parse_sol('src/tests/sqrt2809.sol'))

    def test_solve_returns_correct_truth_assignment_prime961(self):
        cnf, n_vars = parse_cnf('src/tests/prime961.cnf')
        self.assertEqual(solve_sat(cnf, n_vars), parse_sol('src/tests/prime961.sol'))
