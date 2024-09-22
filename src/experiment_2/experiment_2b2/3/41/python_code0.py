import pulp

# Data from the JSON input
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}

# Capacity of each floppy disk
capacity = data['capacity']

# Sizes of files
sizes = data['size']

# Number of files
num_files = len(sizes)

# Create a problem variable to minimize the number of disks used
problem = pulp.LpProblem("Minimize_Disks", pulp.LpMinimize)

# We will use a maximum of `num_files` disks because each file could theoretically be on a separate disk
max_disks = num_files

# Binary variable array indicating if a disk is used
disk_used = pulp.LpVariable.dicts("DiskUsed", range(max_disks), cat='Binary')

# Binary variable matrix indicating if a file is stored on a specific disk
file_on_disk = pulp.LpVariable.dicts("FileOnDisk", (range(num_files), range(max_disks)), cat='Binary')

# Objective function: Minimize the number of disks used
problem += pulp.lpSum(disk_used[d] for d in range(max_disks))

# Constraints
# A file must be on exactly one disk
for f in range(num_files):
    problem += pulp.lpSum(file_on_disk[f][d] for d in range(max_disks)) == 1

# The total size of files on any disk must not exceed the disk's capacity
for d in range(max_disks):
    problem += pulp.lpSum(file_on_disk[f][d] * sizes[f] for f in range(num_files)) <= capacity * disk_used[d]

# Solve the problem
problem.solve()

# Extract the results
n_disks = sum(disk_used[d].value() for d in range(max_disks))
whichdisk = [next(d for d in range(max_disks) if file_on_disk[f][d].value() == 1) for f in range(num_files)]

# Output the results in the specified format
output = {
    "n_disks": int(n_disks),
    "whichdisk": whichdisk
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')