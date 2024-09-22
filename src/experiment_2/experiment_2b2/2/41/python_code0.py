import pulp

# Parse the input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
file_sizes = data['size']
n_files = len(file_sizes)

# Create the problem
problem = pulp.LpProblem("Minimize_Disks_Usage", pulp.LpMinimize)

# Variables
# y_i is 1 if disk i is used, 0 otherwise
y = [pulp.LpVariable(f'y_{i}', cat='Binary') for i in range(n_files)]

# x_ij is 1 if file j is stored in disk i, 0 otherwise
x = [[pulp.LpVariable(f'x_{i}_{j}', cat='Binary') for j in range(n_files)] for i in range(n_files)]

# Objective: Minimize the number of disks used
problem += pulp.lpSum(y)

# Constraints
# Each file j must be stored on exactly one disk
for j in range(n_files):
    problem += pulp.lpSum(x[i][j] for i in range(n_files)) == 1

# The total size of files on each disk i cannot exceed its capacity
for i in range(n_files):
    problem += pulp.lpSum(x[i][j] * file_sizes[j] for j in range(n_files)) <= capacity * y[i]

# Solve the problem
problem.solve()

# Extract results
n_disks = int(pulp.value(pulp.lpSum(y)))
whichdisk = [-1] * n_files

for j in range(n_files):
    for i in range(n_files):
        if pulp.value(x[i][j]) == 1:
            whichdisk[j] = i
            break

# Print the result
output = {"n_disks": n_disks, "whichdisk": whichdisk}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')