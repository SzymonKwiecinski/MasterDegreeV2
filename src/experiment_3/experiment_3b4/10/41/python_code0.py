import pulp

# JSON data
data = {'capacity': 3, 'size': [1, 2, 0.5, 1.5, 2.5]}
capacity = data['capacity']
sizes = data['size']
N = len(sizes)
M = N  # Assume M is equal to N for the model

# Problem
problem = pulp.LpProblem("Minimize_Y_Sum", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in range(M) for j in range(N)], cat='Binary')
y = pulp.LpVariable.dicts("y", [i for i in range(M)], cat='Binary')

# Objective function
problem += pulp.lpSum([y[i] for i in range(M)])

# Constraints
for j in range(N):
    problem += pulp.lpSum([x[i, j] for i in range(M)]) == 1

for i in range(M):
    problem += pulp.lpSum([sizes[j] * x[i, j] for j in range(N)]) <= capacity * y[i]

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')