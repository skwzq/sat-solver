def parse_cnf(path):
    with open(path, 'r') as file:
        data = file.read()

    data = data.splitlines()

    i = 0
    while i < len(data):
        if data[i][0] == 'p':
            break
        i += 1

    n_vars = int(data[i].split()[2])

    f = []

    for j in range(i+1, len(data)):
        clause = [int(x) for x in data[j].split()[:-1]]
        f.append(clause)

    return (f, n_vars)

def parse_sol(path):
    with open(path, 'r') as file:
        data = file.read()

    data = data.splitlines()[1:]

    s = []

    for line in data:
        s += [int(x) for x in line.split()[1:]]
    s.pop()

    return s
