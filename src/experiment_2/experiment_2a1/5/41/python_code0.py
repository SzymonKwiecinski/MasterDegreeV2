import pulp
import json

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']

# Define the problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Variables
n_files = len(sizes)
n_disks = pulp.LpVariable("n_disks", lowBound=1, cat='Integer')
disk_usage = pulp.LpVariable.dicts("disk_usage", (range(n_files), range(n_files)), cat='Binary')

# Objective function: minimize the number of disks used
problem += n_disks, "MinimizeDisks"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(n_files):
    problem += pulp.lpSum(disk_usage[j][i] for i in range(n_disks)) == 1, f"AssignFile_{j}"

# Capacity constraints for each disk
for i in range(n_disks):
    problem += pulp.lpSum(sizes[j] * disk_usage[j][i] for j in range(n_files)) <= capacity, f"DiskCapacity_{i}"

# Solve the problem
problem.solve()

# Output results
n_disks_used = int(pulp.value(n_disks))
which_disk = [next(i for i in range(n_disks_used) if pulp.value(disk_usage[j][i]) == 1) for j in range(n_files)]

output = {
    "n_disks": n_disks_used,
    "whichdisk": which_disk
}

# Print the objective value and output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps(output))