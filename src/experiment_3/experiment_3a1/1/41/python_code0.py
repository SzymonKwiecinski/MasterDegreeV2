import pulp

# Load data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
C = data['capacity']  # Capacity of each floppy disk
sizes = data['size']  # Sizes of the files
N = len(sizes)  # Number of files

# Create the problem
problem = pulp.LpProblem("FloppyDiskDistribution", pulp.LpMinimize)

# Decision Variables
# Define binary variables for file assignment to disks
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
# Define binary variables for whether a disk is used
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective Function: Minimize the number of disks used
problem += pulp.lpSum(y[i] for i in range(N)), "Minimize_Disks"

# Constraints
# 1. Each file must be assigned to exactly one floppy disk
for j in range(N):
    problem += pulp.lpSum(x[j][i] for i in range(N)) == 1, f"File_Assignment_{j}"

# 2. The total size of files on each floppy disk cannot exceed its capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[j][i] for j in range(N)) <= C, f"Disk_Capacity_{i}"

# 3. Ensure a floppy disk is only used if it contains at least one file
for i in range(N):
    problem += pulp.lpSum(x[j][i] for j in range(N)) <= N * y[i], f"Disk_Usage_{i}"

# 4. Count the number of disks used
problem += pulp.lpSum(y[i] for i in range(N)) == pulp.lpSum(y[i] for i in range(N)), "Count_Disks"

# Solve the problem
problem.solve()

# Output the results
n_disks_used = pulp.value(problem.objective)
which_disk = [0] * N  # Assignments to disks

for j in range(N):
    for i in range(N):
        if pulp.value(x[j][i]) == 1:
            which_disk[j] = i + 1  # Store the disk index (1-based)

# Printing results
print(f' (Objective Value): <OBJ>{n_disks_used}</OBJ>')
print(f'Disk assignments: {which_disk}')