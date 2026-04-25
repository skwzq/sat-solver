class Solver:
    def __init__(self, f, n_vars):
        self.trail = []
        self.n_vars = n_vars
        self.watched_in = {x: [] for x in range(-n_vars, n_vars+1)}
        for clause in f:
            for i in range(min(2, len(clause))):
                self.watched_in[clause[i]].append(clause)


    def solve(self):
        while True:
            # unit propagation
            done = False
            while not done:
                trail_length_before = len(self.trail)
                backjumped = False

                for assigned_literal, reason in self.trail:
                    for clause in self.watched_in[-assigned_literal]:
                        non_false_watched = 0
                        non_false_unwatched = 0

                        for literal in clause:
                            if -literal in (x[0] for x in self.trail):
                                continue
                            if clause not in self.watched_in[literal]:
                                # found a new literal to watch
                                non_false_unwatched = literal
                                break
                            non_false_watched = literal  # found a non-false watched literal

                        if non_false_unwatched != 0:
                            # change watched literal
                            self.watched_in[non_false_unwatched].append(clause)
                            self.watched_in[-assigned_literal].remove(clause)
                        elif non_false_watched != 0:
                            # unit clause
                            # add true literal to trail (if it isn't there already) with the clause that implies it must be true
                            if non_false_watched not in (x[0] for x in self.trail):
                                self.trail.append((non_false_watched, clause))
                        else:
                            # every literal in clause is false, try to add a learned clause
                            learned_clause = self.build_learned_clause(clause)
                            if not learned_clause:
                                return None

                            # add clause to formula by adding it to watched clauses
                            for i in range(min(2, len(learned_clause))):
                                self.watched_in[learned_clause[i]].append(learned_clause)

                            if len(learned_clause) == 1:
                                # backjump to before the first decision literal
                                for i in range(len(self.trail)):
                                    if not self.trail[i][1]:
                                        self.trail = self.trail[:i]
                                        break
                                # the literal needs to be added to trail here since it won't be added by unit propagation
                                self.trail.append((learned_clause[0], learned_clause))
                            else:
                                # backtrack to before last decision
                                while self.trail[-1][1]:
                                    self.trail.pop()
                                self.trail.pop()

                            backjumped = True
                            break

                    if backjumped:
                        break

                if not backjumped and len(self.trail) == trail_length_before:
                    done = True

            if len(self.trail) == self.n_vars:
                # all variables have truth values
                return sorted((x[0] for x in self.trail), key=lambda z: abs(z))

            # choose the variable to assign next
            assigned_vars = set(abs(x[0]) for x in self.trail)
            for i in range(1, self.n_vars+1):  # pragma: no cover
                # excluded from coverage because this is always executed at least once
                if i not in assigned_vars:
                    self.trail.append((i, None))
                    break


    def build_learned_clause(self, falsified_clause):
        decision_literal_index = []
        for i in range(len(self.trail)):
            if not self.trail[i][1]:
                decision_literal_index.append(i)

        if len(decision_literal_index) == 0:
            return None

        highest_decision_level_literals = set((x[0] for x in self.trail[decision_literal_index[-1]:]))
        reason_literals = set((-x for x in falsified_clause if -x in highest_decision_level_literals))
        learned_clause = set()

        for i in range(len(self.trail)-1, -1, -1):
            if self.trail[i][0] not in reason_literals:
                continue
            reason_literals.remove(self.trail[i][0])
            if len(reason_literals) == 0:
                learned_clause = list(learned_clause) + [-self.trail[i][0]]
                break
            for x in self.trail[i][1]:
                if -x in highest_decision_level_literals:
                    reason_literals.add(-x)
                elif x != self.trail[i][0]:
                    learned_clause.add(x)

        return learned_clause
