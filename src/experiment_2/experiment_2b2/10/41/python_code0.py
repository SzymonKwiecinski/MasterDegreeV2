import pulp

# Input data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Define the problem
problem = pulp.LpProblem("Minimize_Floppy_Disks", pulp.LpMinimize)

# Define decision variables
# y[i] = 1 if disk i is used, 0 otherwise
y = [pulp.LpVariable(f'y_{i}', cat='Binary') for i in range(N)]

# x[j][i] = 1 if file j is placed on disk i, 0 otherwise
x = [[pulp.LpVariable(f'x_{j}_{i}', cat='Binary') for i in range(N)] for j in range(N)]

# Objective: Minimize the number of disks used
problem += pulp.lpSum(y)

# Each file must be placed on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[j][i] for i in range(N)) == 1, f'FileAssignment_{j}'

# Disk capacity constraints
for i in range(N):
    problem += pulp.lpSum(x[j][i] * sizes[j] for j in range(N)) <= capacity * y[i], f'DiskCapacity_{i}'

# Solve the problem
problem.solve()

# Extract results
n_disks = sum(y[i].varValue for i in range(N))
whichdisk = [next(i for i in range(N) if x[j][i].varValue > 0.5) for j in range(N)]

# Create output
output = {
    "n_disks": int(n_disks),
    "whichdisk": whichdisk
}

print(output)

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')