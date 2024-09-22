import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Problem
problem = pulp.LpProblem("Floppy_Disk_Backup", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", (i for i in range(N)), cat='Binary')

# Objective
problem += pulp.lpSum(y[i] for i in range(N))

# Constraints
# 1. Each file must be placed on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1

# 2. The total size of files on each disk must not exceed its capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= capacity * y[i]

# 3. A disk i is used if at least one file is assigned to it
for i in range(N):
    for j in range(N):
        problem += x[i, j] <= y[i]

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')