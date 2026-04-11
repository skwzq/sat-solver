import unittest

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
