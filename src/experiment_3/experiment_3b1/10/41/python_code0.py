import pulp
import json

# Given data
data = json.loads("{'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}")
C = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Decision Variables
n_disks = pulp.LpVariable('n_disks', lowBound=1, cat='Integer')
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective Function
problem += n_disks, "MinimizeNumberOfDisks"

# Constraints
# 1. Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1, f"AssignFile{j}"

# 2. The total size of files on each disk must not exceed its capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= C, f"DiskCapacity{i}"

# 3. A disk can only be used if at least one file is assigned to it
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= N * y[i], f"DiskUsed{i}"

# 4. Limit the number of disks used
problem += n_disks == pulp.lpSum(y[i] for i in range(N)), "NumberOfDisks"

# Solve the problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

for j in range(N):
    for i in range(N):
        if pulp.value(x[i, j]) == 1:
            print(f'File {j} is placed on Disk {i}')