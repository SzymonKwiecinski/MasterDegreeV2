import pulp

# Data from JSON
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
size = data['size']
N = len(size)

# Create the problem
problem = pulp.LpProblem("FloppyDiskBackupProblem", pulp.LpMinimize)

# Decision variables
n_disks = pulp.LpVariable("n_disks", lowBound=0, cat='Integer')
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Objective Function
problem += n_disks, "Minimize total number of disks used"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[j][k] for k in range(N)) == 1, f"AssignFile_{j}"

# The total size of files assigned to each disk must not exceed its capacity
for k in range(N):
    problem += pulp.lpSum(size[j] * x[j][k] for j in range(N)) <= capacity, f"DiskCapacity_{k}"

# Ensure that n_disks is properly defined
for k in range(N):
    problem += n_disks >= k * pulp.lpSum(x[j][k] for j in range(N)), f"MinDisks_{k}"

# Solve the problem
problem.solve()

# Output results
whichdisk = [None] * N
for j in range(N):
    for k in range(N):
        if pulp.value(x[j][k]) == 1:
            whichdisk[j] = k

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print("Total number of disks used:", pulp.value(n_disks))
print("Files assigned to disks:", whichdisk)