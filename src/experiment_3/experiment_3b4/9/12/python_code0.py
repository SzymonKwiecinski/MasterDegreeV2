import pulp

# Parse the input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}
N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Z", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0)

# Objective function
objective = pulp.lpSum([x[i, N-1] * Rate[i][N-1] for i in range(N-1)]) + Start[N-1] - pulp.lpSum([x[N-1, j] for j in range(N-1)])
problem += objective, "Objective"

# Constraints
# Capacity constraints
for i in range(N):
    problem += pulp.lpSum([x[i, j] for j in range(N)]) <= Limit[i], f"Limit_Constraint_{i}"

# Flow constraints
for i in range(N):
    problem += Start[i] + pulp.lpSum([x[j, i] * Rate[j][i] for j in range(N)]) == pulp.lpSum([x[i, j] for j in range(N)]), f"Flow_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')