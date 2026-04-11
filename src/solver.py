class Solver:
    def __init__(self, f, n_vars):
        self.n_vars = n_vars
        self.watched_in = {x: [] for x in range(-n_vars, n_vars+1)}
        for clause in f:
            for i in range(min(2, len(clause))):
                self.watched_in[clause[i]].append(clause)

    def solve(self, t=[]):
        for val in t:
            for clause in self.watched_in[-val]:
                non_false_watched = 0
                non_false_unwatched = 0

                for literal in clause:
                    if -literal in t:
                        continue
                    if clause not in self.watched_in[literal]:
                        # found a new literal to watch
                        non_false_unwatched = literal
                        break
                    non_false_watched = literal  # found a non-false watched literal

                if non_false_unwatched != 0:
                    # change watched literal
                    self.watched_in[non_false_unwatched].append(clause)
                    self.watched_in[-val].remove(clause)
                elif non_false_watched != 0:
                    # unit clause, add literal to truth assignment if it isn't there already
                    if non_false_watched not in t:
                        t.append(non_false_watched)
                else:
                    # every literal in clause is false
                    return None

        if len(t) == self.n_vars:
            # all variables have truth values
            return t

        # choose the variable to assign next
        assigned_vars = set(abs(x) for x in t)
        for i in range(1, self.n_vars+1):  # pragma: no cover
            # excluded from coverage because this is always executed at least once
            if i not in assigned_vars:
                new = i
                break

        for x in [new, -new]:
            result = self.solve(t+[x])
            if result:
                return sorted(result, key=lambda z: abs(z))

        return None
