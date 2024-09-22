import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
C = data['capacity']
sizes = data['size']
N = len(sizes)

# Define the problem
problem = pulp.LpProblem("MinimizeFloppyDisks", pulp.LpMinimize)

# Decision variables
# Binary variables x_jd: file j assigned to disk d
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Binary variable y_d: disk d is used
y = pulp.LpVariable.dicts("y", range(N), cat='Binary')

# Objective function
problem += pulp.lpSum(y[d] for d in range(N)), "TotalDisks"

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[j][d] for d in range(N)) == 1, f"FileAssignment_{j}"

# Capacity constraints
for d in range(N):
    problem += pulp.lpSum(sizes[j] * x[j][d] for j in range(N)) <= C * y[d], f"Capacity_{d}"

# Ensure disk is counted only if at least one file is assigned
for j in range(N):
    for d in range(N):
        problem += y[d] >= x[j][d], f"DiskUsed_{j}_{d}"

# Solve the problem
problem.solve()

# Output the results
n_disks_used = int(pulp.value(problem.objective))
whichdisk = [0] * N
for j in range(N):
    for d in range(N):
        if pulp.value(x[j][d]) == 1:
            whichdisk[j] = d

print(f' (Objective Value): <OBJ>{n_disks_used}</OBJ>')
print(f'Files are stored in the following disks: {whichdisk}')