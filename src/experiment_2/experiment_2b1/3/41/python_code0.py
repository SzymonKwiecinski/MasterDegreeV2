import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
file_sizes = data['size']

# Number of files
N = len(file_sizes)

# Create the problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Decision variables
# x[i][j] is 1 if file j is placed on disk i, otherwise 0
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')

# y[i] is 1 if disk i is used, otherwise 0
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective function: Minimize the number of disks used
problem += pulp.lpSum(y[i] for i in range(N)), "MinimizeDisks"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N)) == 1, f"FileAssignment_{j}"

# Each disk can hold files up to its capacity
for i in range(N):
    problem += pulp.lpSum(file_sizes[j] * x[i, j] for j in range(N)) <= capacity * y[i], f"DiskCapacity_{i}"

# Solve the problem
problem.solve()

# Prepare output
n_disks = int(pulp.value(problem.objective))
whichdisk = [None] * N
for j in range(N):
    for i in range(N):
        if pulp.value(x[i, j]) == 1:
            whichdisk[j] = i + 1  # disk numbers starting from 1
            break

# Output result
result = {
    "n_disks": n_disks,
    "whichdisk": whichdisk
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')