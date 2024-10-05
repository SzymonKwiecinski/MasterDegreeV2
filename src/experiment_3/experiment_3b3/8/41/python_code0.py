import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
C = data['capacity']
sizes = data['size']
N = len(sizes)
D = N  # Maximum potential disks (one file per disk)

# Problem
problem = pulp.LpProblem("FloppyDiskBackupProblem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("disk_used", range(D), cat=pulp.LpBinary)
y = pulp.LpVariable.dicts("file_on_disk", ((j, d) for j in range(N) for d in range(D)), cat=pulp.LpBinary)

# Objective Function
problem += pulp.lpSum([x[d] for d in range(D)])

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum([y[(j, d)] for d in range(D)]) == 1

# The total size of files on a disk cannot exceed its capacity
for d in range(D):
    problem += pulp.lpSum([sizes[j] * y[(j, d)] for j in range(N)]) <= C * x[d]

# If a disk is used, at least one file must be on it
for j in range(N):
    for d in range(D):
        problem += y[(j, d)] <= x[d]

# Solve
problem.solve()

# Output
n_disks = sum(x[d].varValue for d in range(D))
whichdisk = [d for j in range(N) for d in range(D) if y[(j, d)].varValue == 1]

print(f'Total number of floppy disks used: {n_disks}')
print(f'File assignments to disks: {whichdisk}')
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')