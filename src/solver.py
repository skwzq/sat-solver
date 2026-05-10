def solve_sat(cnf, n_vars):
    """Determines the satisfiability of a CNF formula.

    Args:
        cnf: A CNF formula in the form of a list of clauses, where clauses are lists of integers,
            each of which denotes a literal. (for example, -6 is the negation of variable 6)
        n_vars: The number of variables in the formula.

    Returns:
        If satisfiable: Satisfying truth assignment as an ordered list of integers in the same
            format as in the input formula.
        If unsatisfiable: None.
    """
    # trail_literals: current partial truth assignment
    # trail_reasons: for each literal in trail, either the clause which caused it to be added by
    #   unit propagation, or None if it was explicitly decided
    # watched_in: for each literal in formula, list of clauses where it's watched
    trail_literals = []
    trail_reasons = []
    watched_in = {x: [] for x in range(-n_vars, n_vars+1)}
    for clause in cnf:
        for i in range(min(2, len(clause))):
            watched_in[clause[i]].append(clause)

    while True:
        if len(trail_literals) == n_vars:
            # all variables have truth values
            return sorted(trail_literals, key=abs)

        # choose the variable to assign next and add it to trail
        assigned_vars = set(abs(x) for x in trail_literals)
        for i in range(1, n_vars+1):  # pragma: no cover
            # excluded from coverage because n_vars can't be 0 here
            if i not in assigned_vars:
                trail_literals.append(i)
                trail_reasons.append(None)
                break

        if not unit_propagation(trail_literals, trail_reasons, watched_in):
            # unsatisfiable
            return None


def unit_propagation(trail_literals, trail_reasons, watched_in):
    """Changes watched literals, adds unit clause literals to trail and finds conflicts.

    Args:
        See comments in solve_sat.

    Returns:
        False if the formula was found unsatisfiable, otherwise True.
    """
    while True:
        trail_length_before = len(trail_literals)
        backjumped = False

        for trail_literal in trail_literals:
            for clause in watched_in[-trail_literal]:
                # Try to find a replacement for the falsified watched literal.

                # Non-false unwatched literals can become new watched literals; if none are found
                # but a non-false watched literal is found, the clause is a unit clause
                non_false_watched = None
                non_false_unwatched = None

                trail_literals_set = set(trail_literals)

                for literal in clause:
                    if -literal in trail_literals_set:
                        # false literal
                        continue
                    if clause not in watched_in[literal]:
                        # found a new literal to watch
                        non_false_unwatched = literal
                        break
                    # not false, currently watched
                    non_false_watched = literal

                if non_false_unwatched:
                    # change watched literal
                    watched_in[non_false_unwatched].append(clause)
                    watched_in[-trail_literal].remove(clause)
                elif non_false_watched:
                    # unit clause; add true literal to trail (if it isn't there already) with the
                    # clause that implies it must be true
                    if non_false_watched not in trail_literals_set:
                        trail_literals.append(non_false_watched)
                        trail_reasons.append(clause)
                else:
                    # false clause
                    if not add_learned_clause_and_backjump(trail_literals, trail_reasons,
                        watched_in, clause):
                        # unsatisfiable
                        return False
                    backjumped = True
                    break

            if backjumped:
                break

        if not backjumped and len(trail_literals) == trail_length_before:
            # no more literals will be added by unit propagation
            return True


def add_learned_clause_and_backjump(trail_literals, trail_reasons, watched_in, falsified_clause):
    """Adds a learned clause to the formula and then backjumps.

    Args:
        falsified_clause: A clause falsified by the current partial truth assignment.
        For descriptions of the other arguments, see solve_sat.

    Returns:
        False if the formula was found unsatisfiable, otherwise True.
    """
    learned_clause = build_learned_clause(trail_literals, trail_reasons, falsified_clause)
    if not learned_clause:
        # unsatisfiable
        return False

    duplicate = False
    for literal in learned_clause:
        if learned_clause in watched_in[literal]:
            duplicate = True
            break

    if not duplicate:
        # add learned clause to formula by adding it to watched literal clause lists
        for i in range(min(2, len(learned_clause))):
            watched_in[learned_clause[i]].append(learned_clause)

    # find first decision literal
    first_decision_literal_index = 0
    while trail_reasons[first_decision_literal_index]:
        first_decision_literal_index += 1

    if len(learned_clause) == 1:
        # backjump to before the first decision literal
        while len(trail_literals) > first_decision_literal_index:
            trail_literals.pop()
            trail_reasons.pop()
        # the literal needs to be added to trail here since it won't be added by unit
        # propagation
        trail_literals.append(learned_clause[0])
        trail_reasons.append(learned_clause)
    else:
        # backjump to the second highest decision level of the literals in the learned clause
        index = len(trail_literals) - 1
        while trail_reasons[index]:
            index -= 1
        for i in range(index-1, first_decision_literal_index-1, -1):
            if trail_literals[i] in learned_clause:
                break
            if not trail_reasons[i]:
                index = i
        while len(trail_literals) > index:
            trail_literals.pop()
            trail_reasons.pop()

    return True


def build_learned_clause(trail_literals, trail_reasons, falsified_clause):
    """Analyzes the conflict and builds a learned clause.
    
    Args:
        falsified_clause: A clause falsified by the current partial truth assignment.
        For descriptions of the other arguments, see solve_sat.

    Returns:
        None if the formula is unsatisfiable, otherwise the learned clause.
    """
    # find last decision literal
    decision_literal_index = None
    for i in range(len(trail_reasons)-1, -1, -1):
        if not trail_reasons[i]:
            decision_literal_index = i
            break

    if decision_literal_index is None:
        # the conflict results purely from the formula itself, unsatisfiable
        return None

    # highest_decision_level_literals: last decision literal and the rest of the trail after it
    # reason_literals: Highest decision level literals which directly or indirectly lead to the
    #   clause becoming false. Literals are removed when they're encountered in the trail.
    highest_decision_level_literals = set(trail_literals[decision_literal_index:])
    reason_literals = set()
    learned_clause = set()
    for literal in falsified_clause:
        if -literal in highest_decision_level_literals:
            reason_literals.add(-literal)
        else:
            learned_clause.add(literal)

    # find the last highest-level literal such that all the literals after it leading to the
    # clause becoming false are implied by it
    for i in range(len(trail_literals)-1, -1, -1):
        if trail_literals[i] not in reason_literals:
            # irrelevant literal
            continue
        reason_literals.remove(trail_literals[i])
        if len(reason_literals) == 0:
            # found the right one
            learned_clause = list(learned_clause) + [-trail_literals[i]]
            break
        for x in trail_reasons[i]:
            if -x in highest_decision_level_literals:
                reason_literals.add(-x)
            elif x != trail_literals[i]:
                # -x is a lower level literal contributing to the clause becoming false
                learned_clause.add(x)

    return learned_clause
