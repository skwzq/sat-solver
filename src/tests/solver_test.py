import unittest

from parse_files import parse_cnf, parse_sol
from solver import Solver

class TestSolver(unittest.TestCase):
    def test_solve_returns_empty_if_empty_formula(self):
        solver = Solver(f=[], n_vars=0)
        self.assertEqual(solver.solve(), [])

    def test_solve_returns_none_if_unsatisfiable(self):
        solver = Solver(f=[[1, -2], [-1], [2]], n_vars=2)
        self.assertEqual(solver.solve(), None)

    def test_solve_returns_correct_truth_assignment_2_variables(self):
        solver = Solver(f=[[1, -2], [2]], n_vars=2)
        self.assertEqual(solver.solve(), [1, 2])

    def test_solve_returns_correct_truth_assignment_4_variables_and_bigger_clauses(self):
        solver = Solver(f=[[-1, -2, 3, 4], [2, 3], [1, -2], [1, -3], [-3, 4], [-2, -4]], n_vars=4)
        self.assertEqual(solver.solve(), [1, -2, 3, 4])

    def test_solve_returns_correct_truth_assignment_multiple_backjumps(self):
        solver = Solver(f=[[-1, 2], [-2, 3], [-2, 4], [-3, -4], [-3, 4], [-4, 5], [-4, 6], [-5, -6], [6]], n_vars=6)
        self.assertEqual(solver.solve(), [-1, -2, -3, -4, -5, 6])

    # the files used in the following tests are from https://github.com/arminbiere/cadical/tree/master/test/cnf

    def test_solve_returns_correct_truth_assignment_sqrt2809(self):
        f, n_vars = parse_cnf('src/tests/sqrt2809.cnf')
        solver = Solver(f, n_vars)
        self.assertEqual(solver.solve(), parse_sol('src/tests/sqrt2809.sol'))

    def test_solve_returns_correct_truth_assignment_prime961(self):
        f, n_vars = parse_cnf('src/tests/prime961.cnf')
        solver = Solver(f, n_vars)
        self.assertEqual(solver.solve(), parse_sol('src/tests/prime961.sol'))
