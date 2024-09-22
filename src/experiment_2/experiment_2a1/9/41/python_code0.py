import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']

# Create the problem
problem = pulp.LpProblem("FloppyDiskPacking", pulp.LpMinimize)

# Variables
n_files = len(sizes)
n_disks = pulp.LpVariable('n_disks', lowBound=1, cat='Integer')  # Total number of disks used
x = pulp.LpVariable.dicts('x', (range(n_files), range(n_files)), cat='Binary')  # x[i][j] = 1 if file i is placed on disk j

# Objective function: minimize the number of disks used
problem += n_disks, "MinimizeDisks"

# Constraints
# Each file must be placed on exactly one disk
for i in range(n_files):
    problem += pulp.lpSum(x[i][j] for j in range(n_disks)) == 1, f"File_{i}_Placement"

# The total size of files on each disk must not exceed the disk capacity
for j in range(n_disks):
    problem += pulp.lpSum(sizes[i] * x[i][j] for i in range(n_files)) <= capacity, f"Disk_{j}_Capacity"

# Each disk can only be used if it has at least one file
for j in range(n_disks):
    problem += pulp.lpSum(x[i][j] for i in range(n_files)) <= n_disks, f"Disk_{j}_Usage"

# Solve the problem
problem.solve()

# Prepare the output
n_disks_used = int(pulp.value(n_disks))
which_disk = [0] * n_files

for i in range(n_files):
    for j in range(n_disks_used):
        if pulp.value(x[i][j]) == 1:
            which_disk[i] = j + 1  # Disk numbers should start from 1

# Output result
result = {
    'n_disks': n_disks_used,
    'whichdisk': which_disk
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')