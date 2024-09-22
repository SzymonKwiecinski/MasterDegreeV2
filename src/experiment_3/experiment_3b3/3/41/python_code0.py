import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
C = data['capacity']
size = data['size']
N = len(size)

# Create the LP problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Variables
max_possible_disks = N  # A worst-case maximum, one file per disk
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(max_possible_disks) for j in range(N)), cat='Binary')
n_disks = pulp.LpVariable("n_disks", lowBound=1, cat='Integer')

# Objective Function
problem += n_disks

# Constraints
# Each file must be allocated to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(max_possible_disks)) == 1

# The total size of files on each disk cannot exceed its capacity
for i in range(max_possible_disks):
    problem += pulp.lpSum(size[j] * x[i, j] for j in range(N)) <= C

# Number of disks constraint
problem += n_disks >= 1
for i in range(max_possible_disks):
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= n_disks

# Solve the problem
problem.solve()

# Extract the results
whichdisk = [i for j in range(N) for i in range(max_possible_disks) if pulp.value(x[i, j]) == 1]
print(f'n_disks: {int(pulp.value(n_disks))}')
print(f'whichdisk: {whichdisk}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')