class Solver:
    """Class for determining the satisfiability of a CNF formula."""

    def __init__(self, f, n_vars):
        """Initializes the instance for the given formula.
        
        Args:
            f: A CNF formula in the form of a list of clauses, where clauses are lists of integers,
              each of which denotes a literal. (for example, -6 means the negation of variable 6)
            n_vars: The number of variables in the formula.
        """
        self.__trail_literals = []
        self.__trail_reason = []
        self.__n_vars = n_vars
        self.__watched_in = {x: [] for x in range(-n_vars, n_vars+1)}
        for clause in f:
            for i in range(min(2, len(clause))):
                self.__watched_in[clause[i]].append(clause)


    def solve(self):
        """Determines whether the formula is satisfiable.

        Returns:
            If satisfiable: Satisfying truth assignment as an ordered list of integers in the same
              format as in the input formula.
            If unsatisfiable: None.
        """
        while True:
            if len(self.__trail_literals) == self.__n_vars:
                # all variables have truth values
                return sorted(self.__trail_literals, key=abs)

            # choose the variable to assign next
            assigned_vars = set(abs(x) for x in self.__trail_literals)
            for i in range(1, self.__n_vars+1):  # pragma: no cover
                # excluded from coverage because this is always executed at least once
                if i not in assigned_vars:
                    self.__trail_literals.append(i)
                    self.__trail_reason.append(None)
                    break

            if not self.__unit_propagation():
                return None


    def __unit_propagation(self):
        while True:
            trail_length_before = len(self.__trail_literals)
            backtracked = False

            for assigned_literal in self.__trail_literals:
                for clause in self.__watched_in[-assigned_literal]:
                    non_false_watched = 0
                    non_false_unwatched = 0

                    for literal in clause:
                        if -literal in self.__trail_literals:
                            continue
                        if clause not in self.__watched_in[literal]:
                            # found a new literal to watch
                            non_false_unwatched = literal
                            break
                        non_false_watched = literal  # found a non-false watched literal

                    if non_false_unwatched != 0:
                        # change watched literal
                        self.__watched_in[non_false_unwatched].append(clause)
                        self.__watched_in[-assigned_literal].remove(clause)
                    elif non_false_watched != 0:
                        # unit clause; add true literal to trail (if it isn't there already) with
                        # the clause that implies it must be true
                        if non_false_watched not in self.__trail_literals:
                            self.__trail_literals.append(non_false_watched)
                            self.__trail_reason.append(clause)
                    else:
                        if not self.__add_learned_clause_and_backtrack(clause):
                            return False
                        backtracked = True
                        break

                if backtracked:
                    break

            if not backtracked and len(self.__trail_literals) == trail_length_before:
                return True


    def __add_learned_clause_and_backtrack(self, falsified_clause):
        learned_clause = self.__build_learned_clause(falsified_clause)
        if not learned_clause:
            return False

        # add learned clause to formula by adding it to watched clauses
        for i in range(min(2, len(learned_clause))):
            self.__watched_in[learned_clause[i]].append(learned_clause)

        if len(learned_clause) == 1:
            # backjump to before the first decision literal
            for i, reason in enumerate(self.__trail_reason):
                if not reason:
                    self.__trail_literals = self.__trail_literals[:i]
                    self.__trail_reason = self.__trail_reason[:i]
                    break
            # the literal needs to be added to trail here since it won't be added by unit
            # propagation
            self.__trail_literals.append(learned_clause[0])
            self.__trail_reason.append(learned_clause)
        else:
            # backtrack to before last decision
            while self.__trail_reason[-1]:
                self.__trail_literals.pop()
                self.__trail_reason.pop()
            self.__trail_literals.pop()
            self.__trail_reason.pop()

        return True


    def __build_learned_clause(self, falsified_clause):
        decision_literal_index = []
        for i, reason in enumerate(self.__trail_reason):
            if not reason:
                decision_literal_index.append(i)

        if len(decision_literal_index) == 0:
            return None

        highest_decision_level_literals = set(self.__trail_literals[decision_literal_index[-1]:])
        reason_literals = set((-x for x in falsified_clause if -x in highest_decision_level_literals))
        learned_clause = set()

        for i in range(len(self.__trail_literals)-1, -1, -1):
            if self.__trail_literals[i] not in reason_literals:
                continue
            reason_literals.remove(self.__trail_literals[i])
            if len(reason_literals) == 0:
                learned_clause = list(learned_clause) + [-self.__trail_literals[i]]
                break
            for x in self.__trail_reason[i]:
                if -x in highest_decision_level_literals:
                    reason_literals.add(-x)
                elif x != self.__trail_literals[i]:
                    learned_clause.add(x)

        return learned_clause
