import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
file_sizes = data['size']

# Define the problem
problem = pulp.LpProblem("FloppyDiskPacking", pulp.LpMinimize)

# Number of files
num_files = len(file_sizes)

# Variables
n_disks = pulp.LpVariable('n_disks', lowBound=1, cat='Integer')  # Total number of disks used
x = pulp.LpVariable.dicts("x", (range(num_files), range(num_files)), cat='Binary')  # 1 if file j is on disk i

# Objective: Minimize the number of disks used
problem += n_disks

# Constraints
# Ensure each file is assigned to exactly one disk
for j in range(num_files):
    problem += pulp.lpSum(x[j][i] for i in range(num_files)) == 1

# Capacity constraints for each disk
for i in range(num_files):
    problem += pulp.lpSum(file_sizes[j] * x[j][i] for j in range(num_files)) <= capacity

# Ensure that we only use n_disks disks
for i in range(num_files):
    for j in range(num_files):
        problem += x[j][i] <= n_disks

# Solve the problem
problem.solve()

# Results
n_disks_used = int(pulp.value(n_disks))
which_disk = [0] * num_files

for j in range(num_files):
    for i in range(num_files):
        if pulp.value(x[j][i]) == 1:
            which_disk[j] = i + 1  # Disk numbering starts from 1

# Output the results
output = {
    "n_disks": n_disks_used,
    "whichdisk": which_disk
}
print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')