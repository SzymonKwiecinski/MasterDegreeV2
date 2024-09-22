import pulp

# Data from JSON format
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
file_sizes = data['size']

# Problem parameters
N = len(file_sizes)  # Number of files
M = N  # Assume worst case where each file could go on a different disk

# Create the problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(M), range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')

# Objective Function: Minimize the number of disks used
problem += pulp.lpSum(y[i] for i in range(M))

# Constraints
# Each file must be placed exactly on one disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(M)) == 1

# The sum of file sizes on a disk cannot exceed its capacity
for i in range(M):
    problem += pulp.lpSum(file_sizes[j] * x[i][j] for j in range(N)) <= capacity * y[i]

# A file can only be assigned to a disk if that disk is used
for i in range(M):
    for j in range(N):
        problem += x[i][j] <= y[i]

# Solve the problem
problem.solve()

# Output
n_disks = sum(pulp.value(y[i]) for i in range(M))
which_disk = {j: next(i for i in range(M) if pulp.value(x[i][j]) == 1) for j in range(N)}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')