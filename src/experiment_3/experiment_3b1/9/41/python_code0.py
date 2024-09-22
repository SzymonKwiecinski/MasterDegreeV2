import pulp

# Data from the provided JSON
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
size = data['size']
N = len(size)

# Initialize the problem
problem = pulp.LpProblem("FloppyDiskBackup", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('disk', range(N), cat='Binary')  # whether a disk is used
y = pulp.LpVariable.dicts('file', (range(N), range(N)), cat='Binary')  # file assignment to disks

# Objective Function: Minimize the number of disks used
problem += pulp.lpSum(x[i] for i in range(N))

# Constraints
# Each file must be assigned to exactly one disk
for j in range(N):
    problem += pulp.lpSum(y[i][j] for i in range(N)) == 1

# The total size of files on each disk must not exceed its capacity
for i in range(N):
    problem += pulp.lpSum(size[j] * y[i][j] for j in range(N)) <= capacity * x[i]

# Solve the problem
problem.solve()

# Output the results
n_disks_used = sum(pulp.value(x[i]) for i in range(N))
which_disk = [next(i for i in range(N) if pulp.value(y[i][j]) == 1) for j in range(N)]

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Total disks used: {n_disks_used}')
print(f'File assignments to disks: {which_disk}')