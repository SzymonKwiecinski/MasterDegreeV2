import pulp

# Extracting data from JSON
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']

# Parameters
M = len(sizes)  # Maximum potential number of disks
N = len(sizes)  # Number of files

# Problem
problem = pulp.LpProblem("Floppy_Disk_Backup_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(M) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", (i for i in range(M)), cat='Binary')

# Objective
problem += pulp.lpSum(y[i] for i in range(M)), "Minimize number of disks used"

# Constraints
# Each file must be on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(M)) == 1, f"File_{j}_on_one_disk"

# Capacity constraint for each disk
for i in range(M):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= capacity * y[i], f"Disk_{i}_capacity"

# File can be on a disk only if the disk is used
for i in range(M):
    for j in range(N):
        problem += x[i, j] <= y[i], f"File_{j}_on_disk_{i}_only_if_used"

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')