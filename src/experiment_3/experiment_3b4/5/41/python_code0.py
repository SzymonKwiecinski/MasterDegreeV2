import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)
M = N  # Upper bound on the number of floppy disks

# Initialize the problem
problem = pulp.LpProblem("Minimize_Floppy_Disks_Usage", pulp.LpMinimize)

# Decision variables
y = pulp.LpVariable.dicts("y", range(M), cat='Binary')
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(M) for j in range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum(y[i] for i in range(M))

# Constraints
# Each file must be placed on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(M)) == 1

# Disk capacity constraints
for i in range(M):
    problem += pulp.lpSum(sizes[j] * x[i, j] for j in range(N)) <= capacity * y[i]

# Linking x and y variables
for i in range(M):
    for j in range(N):
        problem += x[i, j] <= y[i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')