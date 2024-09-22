import pulp

# Parsing the data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
file_sizes = data['size']
num_files = len(file_sizes)

# Problem Definition
problem = pulp.LpProblem("Disk_Allocation_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(num_files) for j in range(num_files)), cat='Binary')
y = pulp.LpVariable.dicts("y", (i for i in range(num_files)), cat='Binary')

# Objective Function
problem += pulp.lpSum([y[i] for i in range(num_files)])

# Constraints
# Each file must be on one disk
for j in range(num_files):
    problem += pulp.lpSum([x[i, j] for i in range(num_files)]) == 1

# Disk capacity constraints
for i in range(num_files):
    problem += pulp.lpSum([file_sizes[j] * x[i, j] for j in range(num_files)]) <= capacity * y[i]

# Disk usage constraints
for i in range(num_files):
    for j in range(num_files):
        problem += x[i, j] <= y[i]

# Solving the problem
problem.solve()

# Gathering results
n_disks = sum(int(pulp.value(y[i])) for i in range(num_files))
whichdisk = {j: None for j in range(num_files)}

for j in range(num_files):
    for i in range(num_files):
        if pulp.value(x[i, j]) == 1:
            whichdisk[j] = i
            break

# Output the results
print(f"Total number of disks used: {n_disks}")
print(f"Assignment of each file to disks: {whichdisk}")
print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")