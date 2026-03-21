from sys import argv

with open(argv[1], 'r') as file:
    input_ = file.read()

input_ = input_.split()

n_vars = int(input_[2])

f = [[]]
watched_in = {x: [] for x in range(-n_vars, n_vars+1)}

for i in range(4, len(input_)-1): # the last number is always 0
    literal = int(input_[i])
    if literal == 0:
        f.append([])
    else:
        f[-1].append(literal)

for clause in f:
    if len(clause) == 1:
        continue
    for i in [0, 1]:
        watched_in[clause[i]].append(clause)


undefined = set(range(1, n_vars+1))

def solve(f, t=[]):
    truth = t

    # unit propagation
    while len(truth) > 0:
        # new array for unit clause literals
        truth_new = []

        t_set = set(t)

        # update watched literals and find unit clauses
        for literal in truth:
            for clause in watched_in[-literal]:
                non_false_literals = 0
                for literal_ in clause:
                    if -literal_ in t_set:
                        continue
                    if clause not in watched_in[literal_]:
                        watched_in[literal_].append(clause)
                        watched_in[-literal].remove(clause)
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

    if len(t) == n_vars:
        return True

    undefined.difference_update(set(abs(x) for x in t))

    new = list(undefined)[0] # choose an undefined variable
    undefined.remove(new)

    if solve(f, t+[new]) or solve(f, t+[-new]):
        return True

    undefined.add(new)

    return False

sat = solve(f)

print(sat)
