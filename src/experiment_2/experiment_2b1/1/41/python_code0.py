import pulp
import json

# Input data in JSON format
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}

# Extract capacity and sizes
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Create the problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Variables: Disk usage indicator (1 if used, 0 otherwise) and file assignment to disk
n_disks = pulp.LpVariable("n_disks", lowBound=0, cat='Integer')
assign = pulp.LpVariable.dicts("assign", (range(N), range(N)), cat='Binary')

# Objective function: Minimize the number of disks used
problem += n_disks, "MinimizeDisks"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(assign[j][i] for i in range(N)) == 1, f"FileAssignment_{j}"

# Capacity constraints for each disk
for i in range(N):
    problem += (pulp.lpSum(sizes[j] * assign[j][i] for j in range(N)) <= capacity, f"DiskCapacity_{i}")

# Ensure that the number of disks used is equal to the number of disks assigned
for i in range(N):
    problem += n_disks >= pulp.lpSum(assign[j][i] for j in range(N)), f"DiskUsage_{i}"

# Solve the problem
problem.solve()

# Prepare output
n_disks_used = int(pulp.value(n_disks))
which_disk = [0] * N

for j in range(N):
    for i in range(n_disks_used):
        if pulp.value(assign[j][i]) == 1:
            which_disk[j] = i + 1  # disks are 1-indexed in the output

# Output result
result = {
    "n_disks": n_disks_used,
    "whichdisk": which_disk
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')