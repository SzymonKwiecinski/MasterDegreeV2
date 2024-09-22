import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
C = data['capacity']
sizes = data['size']
N = len(sizes)
M = N  # Upper bound for number of disks

# Problem definition
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Decision variables
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')  # Disk usage
x = pulp.LpVariable.dicts("x", (range(M), range(N)), cat='Binary')  # File assignment

# Objective function: Minimize number of disks used
problem += pulp.lpSum(y[i] for i in range(M)), "MinimizeDiskUsage"

# Constraints
# 1. Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(M)) == 1, f"AssignFile_{j}"

# 2. Total size on each disk cannot exceed capacity
for i in range(M):
    problem += pulp.lpSum(sizes[j] * x[i][j] for j in range(N)) <= C * y[i], f"DiskCapacity_{i}"

# 3. Relationship between number of disks used and y_i
for i in range(M):
    problem += pulp.lpSum(y[i]) >= y[i], f"DiskRelation_{i}"

# Solve the problem
problem.solve()

# Outputs
n_disks = pulp.value(problem.objective)
whichdisk = [None] * N
for j in range(N):
    for i in range(M):
        if pulp.value(x[i][j]) == 1:
            whichdisk[j] = i

print(f' (Objective Value): <OBJ>{n_disks}</OBJ>')
print(f' (Files assigned to disks): {whichdisk}')