import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
file_sizes = data['size']
num_files = len(file_sizes)

# Problem
problem = pulp.LpProblem("Disk_Usage_Minimization", pulp.LpMinimize)

# Decision Variables
# Maximum number of disks that might be used is assumed to be equal to num_files
M = num_files
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(M) for j in range(num_files)), cat='Binary')
y = pulp.LpVariable.dicts("y", (i for i in range(M)), cat='Binary')

# Objective Function
problem += pulp.lpSum(y[i] for i in range(M))

# Constraints
# Each file must be on exactly one disk
for j in range(num_files):
    problem += pulp.lpSum(x[(i, j)] for i in range(M)) == 1

# The total size of files on each disk cannot exceed its capacity
for i in range(M):
    problem += pulp.lpSum(file_sizes[j] * x[(i, j)] for j in range(num_files)) <= capacity * y[i]

# A disk is considered used if any file is assigned to it
for i in range(M):
    for j in range(num_files):
        problem += x[(i, j)] <= y[i]

# Solve the problem
problem.solve()

# Print the optimal objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')