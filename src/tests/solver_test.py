import unittest

from solver import Solver

class TestSolver(unittest.TestCase):
    def test_solve_returns_correct_truth_assignment_if_satisfiable(self):
        solver = Solver(f=[[1, -2], [2]], n_vars=2)
        self.assertEqual(solver.solve(), [1, 2])

    def test_solve_returns_none_if_unsatisfiable(self):
        solver = Solver(f=[[1, -2], [-1], [2]], n_vars=2)
        self.assertEqual(solver.solve(), None)
