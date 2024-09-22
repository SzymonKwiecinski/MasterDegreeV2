import pulp
import json

# Data extraction from JSON format
data = json.loads('{"capacity": 3, "size": [1, 2, 0.5, 1.5, 2.5]}')
C = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the linear programming problem
problem = pulp.LpProblem("FloppyDiskBackupProblem", pulp.LpMinimize)

# Variables
n_disks = pulp.LpVariable('n_disks', lowBound=1, cat='Integer')
x = pulp.LpVariable.dicts("x", (range(1, N + 1), range(1, N + 1)), 0, 1, pulp.LpBinary)

# Objective function: Minimize the total number of disks used
problem += n_disks, "TotalDisks"

# Constraints
# Each disk's capacity constraint
for i in range(1, N + 1):
    problem += pulp.lpSum(x[i][j] * sizes[j - 1] for j in range(1, N + 1)) <= C, f"DiskCapacityConstraint_{i}"

# Each file must be assigned to exactly one disk
for j in range(1, N + 1):
    problem += pulp.lpSum(x[i][j] for i in range(1, N + 1)) == 1, f"FileAssignmentConstraint_{j}"

# Solve the problem
problem.solve()

# Output results
n_disks_value = pulp.value(problem.objective)
print(f' (Objective Value): <OBJ>{n_disks_value}</OBJ>')

# Which disk each file is placed on
for j in range(1, N + 1):
    for i in range(1, N + 1):
        if pulp.value(x[i][j]) == 1:
            print(f'File {j} is placed on disk {i}.')