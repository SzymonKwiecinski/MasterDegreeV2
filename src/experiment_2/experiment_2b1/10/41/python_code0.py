import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']

# Create the problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Variables
n_disks = pulp.LpVariable("n_disks", lowBound=1, cat='Integer')  # Total number of disks used
x = pulp.LpVariable.dicts("x", ((i, d) for i in range(len(sizes)) for d in range(n_disks)), cat='Binary')  # Which disk each file goes into

# Objective function: minimize the number of disks used
problem += n_disks

# Constraints
for i in range(len(sizes)):
    # Each file must be assigned to exactly one disk
    problem += pulp.lpSum([x[i, d] for d in range(n_disks)]) == 1

for d in range(n_disks):
    # The total size on each disk must not exceed its capacity
    problem += pulp.lpSum([sizes[i] * x[i, d] for i in range(len(sizes))]) <= capacity

# Solve the problem
problem.solve()

# Output the results
n_disks_used = int(pulp.value(n_disks))
which_disk = [0] * len(sizes)

for i in range(len(sizes)):
    for d in range(n_disks_used):
        if pulp.value(x[i, d]) == 1:
            which_disk[i] = d + 1  # Use 1-based indexing for disks

output = {
    "n_disks": n_disks_used,
    "whichdisk": which_disk
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')