import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Problem
problem = pulp.LpProblem("FloppyDiskBackupProblem", pulp.LpMinimize)

# Decision Variables
# Number of disks used
n = pulp.LpVariable('n', lowBound=0, cat=pulp.LpInteger)

# x_{ij} variables
x = pulp.LpVariable.dicts('x', ((i, j) for i in range(N) for j in range(N)), cat=pulp.LpBinary)

# y_i variables
y = pulp.LpVariable.dicts('y', (i for i in range(N)), cat=pulp.LpBinary)

# Objective Function
problem += n, "Minimize number of disks used"

# Constraints

# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[(i, j)] for i in range(N)) == 1

# Total size of files on each disk cannot exceed its capacity
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[(i, j)] for j in range(N)) <= capacity * y[i]

# The number of disks used must equal n
problem += pulp.lpSum(y[i] for i in range(N)) == n

# Link between x_{ij} and y_i
for i in range(N):
    for j in range(N):
        problem += x[(i, j)] <= y[i]

# Solve the problem
problem.solve()

# Output results
whichdisk = [-1] * N
for j in range(N):
    for i in range(N):
        if pulp.value(x[(i, j)]) == 1:
            whichdisk[j] = i

print(f'Total number of floppy disks used: {int(pulp.value(n))}')
print(f'Disk assignment for each file (whichdisk): {whichdisk}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')