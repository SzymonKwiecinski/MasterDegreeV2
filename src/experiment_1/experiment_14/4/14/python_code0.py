import pulp

# Data from JSON
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)

# Problem
problem = pulp.LpProblem("FloppyDiskMinimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat="Binary")
y = pulp.LpVariable.dicts("y", (i for i in range(N)), cat="Binary")

# Objective Function
problem += pulp.lpSum(y[i] for i in range(N))

# Constraints
# Capacity constraint
for i in range(N):
    problem += pulp.lpSum(sizes[j] * x[(i, j)] for j in range(N)) <= capacity * y[i]

# Each file must be on exactly one disk
for j in range(N):
    problem += pulp.lpSum(x[(i, j)] for i in range(N)) == 1

# Solve the problem
problem.solve()

# Output the objective value
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")