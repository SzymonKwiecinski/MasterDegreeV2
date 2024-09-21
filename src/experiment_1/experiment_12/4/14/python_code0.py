import pulp

# Data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Problem
problem = pulp.LpProblem("Minimize_Floppy_Disks", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat=pulp.LpBinary)
y = pulp.LpVariable.dicts("y", range(N), cat=pulp.LpBinary)

# Objective Function
problem += pulp.lpSum(y[i] for i in range(N))

# Constraints
# Constraint 1: Capacity constraint for each floppy disk
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[i][j] for j in range(N)) <= capacity * y[i]

# Constraint 2: Each file must be on exactly one floppy disk
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N)) == 1

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')