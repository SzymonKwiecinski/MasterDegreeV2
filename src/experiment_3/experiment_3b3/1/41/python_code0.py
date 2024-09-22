import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
file_sizes = data['size']
num_files = len(file_sizes)
max_disks = num_files  # Maximum possible disks is equal to the number of files

# Problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Decision Variables
d = pulp.LpVariable.dicts("DiskUsed", range(max_disks), cat=pulp.LpBinary)
x = pulp.LpVariable.dicts("FileOnDisk", ((j, k) for j in range(num_files) for k in range(max_disks)), cat=pulp.LpBinary)

# Objective Function
problem += pulp.lpSum(d[k] for k in range(max_disks)), "Minimize Number of Disks Used"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(num_files):
    problem += pulp.lpSum(x[j, k] for k in range(max_disks)) == 1, f"AssignFile_{j}"

# The total size of the files on each disk must not exceed its capacity
for k in range(max_disks):
    problem += pulp.lpSum(file_sizes[j] * x[j, k] for j in range(num_files)) <= capacity * d[k], f"CapacityDisk_{k}"

# A disk can only be marked as used if at least one file is assigned to it
for j in range(num_files):
    for k in range(max_disks):
        problem += d[k] >= x[j, k], f"DiskUsedWhenFileAssigned_{j}_{k}"

# Solve the problem
problem.solve()

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')