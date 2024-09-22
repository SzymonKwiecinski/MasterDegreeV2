import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
file_sizes = data['size']
N = len(file_sizes)

# Create the problem instance
problem = pulp.LpProblem('FloppyDiskPacking', pulp.LpMinimize)

# Variables
n_disks = pulp.LpVariable('n_disks', lowBound=0, cat='Integer')
x = pulp.LpVariable.dicts('x', ((j, d) for j in range(N) for d in range(N)), cat='Binary')

# Objective function: minimize the number of disks
problem += n_disks

# Constraints
for j in range(N):
    problem += pulp.lpSum(x[j, d] for d in range(N)) == 1  # Each file must be on exactly one disk

for d in range(N):
    problem += pulp.lpSum(file_sizes[j] * x[j, d] for j in range(N)) <= capacity  # Each disk's capacity constraint

# Capacity constraint on the number of disks used
for d in range(N):
    problem += pulp.lpSum(x[j, d] for j in range(N)) <= n_disks  # A disk can only be counted if it has files

# Solve the problem
problem.solve()

# Output data
n_disks_used = int(pulp.value(n_disks))
which_disk = [None] * N

for j in range(N):
    for d in range(N):
        if pulp.value(x[j, d]) == 1:
            which_disk[j] = d

result = {
    "n_disks": n_disks_used,
    "whichdisk": which_disk
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')