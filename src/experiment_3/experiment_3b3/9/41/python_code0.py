import pulp

# Data input
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
file_sizes = data['size']
n = len(file_sizes)
C = data['capacity']

# Assume a large enough number of disks initially
m = n

# Problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(m) for j in range(n)), 0, 1, pulp.LpBinary)
y = pulp.LpVariable.dicts("y", (i for i in range(m)), 0, 1, pulp.LpBinary)

# Objective
problem += pulp.lpSum(y[i] for i in range(m)), "Minimize the number of disks used"

# Constraints
# Each file is assigned to exactly one disk
for j in range(n):
    problem += pulp.lpSum(x[i, j] for i in range(m)) == 1, f"File_{j}_assignment"

# Capacity constraint on each disk
for i in range(m):
    problem += pulp.lpSum(file_sizes[j] * x[i, j] for j in range(n)) <= C * y[i], f"Disk_{i}_capacity"

# Ensure a disk marked as used must contain at least one file
for i in range(m):
    for j in range(n):
        problem += y[i] >= x[i, j], f"Usage_indicator_disk{i}_file{j}"

# Solve
problem.solve()

# Output solutions
n_disks = sum(y[i].varValue for i in range(m))
whichdisk = [i for j in range(n) for i in range(m) if x[i, j].varValue == 1]

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')