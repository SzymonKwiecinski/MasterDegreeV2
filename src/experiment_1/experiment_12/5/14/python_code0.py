import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
size = data['size']
N = len(size)

# Initialize the problem
problem = pulp.LpProblem("Minimize_Floppy_Disks", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
y = pulp.LpVariable.dicts("y", (i for i in range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum([y[i] for i in range(N)])

# Constraints
# Capacity of floppy disks
for i in range(N):
    problem += pulp.lpSum([size[j] * x[i, j] for j in range(N)]) <= capacity * y[i]

# Each file must be placed on exactly one floppy disk
for j in range(N):
    problem += pulp.lpSum([x[i, j] for i in range(N)]) == 1

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')