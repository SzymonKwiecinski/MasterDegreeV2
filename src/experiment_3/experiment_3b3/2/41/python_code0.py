import pulp

# Data from JSON
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
C = data['capacity']
sizes = data['size']
N = len(sizes)  # Number of files

# Problem setup
problem = pulp.LpProblem("Floppy_Disk_Backup_Problem", pulp.LpMinimize)

# Maximum possible disks (upper bound for the problem)
max_disks = N

# Decision variables
# x_ij: Binary variable, 1 if file j is placed on floppy disk i, 0 otherwise
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(max_disks) for j in range(N)), 
                          cat='Binary')

# y_i: Binary variable, 1 if disk i is used, 0 otherwise
y = pulp.LpVariable.dicts("y", (i for i in range(max_disks)), cat='Binary')

# Objective function: Minimize total number of disks used
problem += pulp.lpSum(y[i] for i in range(max_disks)), "Minimize_number_of_disks"

# Constraints
# 1. Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(max_disks)) == 1, f"File_assignment_{j}"

# 2. The total size of files assigned to each disk must not exceed its capacity
for i in range(max_disks):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= C * y[i], f"Capacity_constraint_{i}"

# 3. The total number of disks used must be sufficient to cover all used disks
for i in range(max_disks):
    problem += y[i] <= 1, f"Disk_usage_constraint_{i}"

# Solve the problem
problem.solve()

# Objective value (number of disks used)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output: Which disk each file is assigned to
which_disk = [-1] * N
for j in range(N):
    for i in range(max_disks):
        if pulp.value(x[i, j]) == 1:
            which_disk[j] = i
            break

print("Files distribution on disks:", which_disk)