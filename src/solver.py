class Solver:
    def __init__(self, f, n_vars):
        self.n_vars = n_vars
        self.watched_in = {x: [] for x in range(-n_vars, n_vars+1)}
        for clause in f:
            if len(clause) == 1:
                continue
            for i in [0, 1]:
                self.watched_in[clause[i]].append(clause)

    def solve(self, t=[]):
        truth = t

        # unit propagation
        while len(truth) > 0:
            # new array for unit clause literals
            truth_new = []

            t_set = set(t)

            # update watched literals and find unit clauses
            for literal in truth:
                for clause in self.watched_in[-literal]:
                    non_false_literals = 0
                    for literal_ in clause:
                        if -literal_ in t_set:
                            continue
                        if clause not in self.watched_in[literal_]:
                            self.watched_in[literal_].append(clause)
                            self.watched_in[-literal].remove(clause)
                            non_false_literals = 2  # at least 2 must be non-false
                            break
                        non_false_literals += 1

                    if non_false_literals == 0:
                        return False

                    if non_false_literals == 1:
                        truth_new.append(clause[0])

            for literal in truth_new:
                t.append(literal)

            truth = truth_new

        if len(t) == self.n_vars:
            return t

        t_vars = set(abs(x) for x in t)

        # choose an unassigned variable
        for x in range(1, self.n_vars+1):
            if x not in t_vars:
                new = x
                break

        for x in [new, -new]:
            next_ = self.solve(t+[x])
            if next_:
                return next_

        return None
