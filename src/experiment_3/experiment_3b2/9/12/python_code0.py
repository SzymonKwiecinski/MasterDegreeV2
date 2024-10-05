import pulp

# Data from JSON format
data = {
    'N': 3,
    'Start': [100.0, 50.0, 200.0],
    'Limit': [1000.0, 200.0, 3000.0],
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Create a linear programming problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(x[i][N-1] * Rate[i][N-1] for i in range(N-1)) + Start[N-1] + \
            pulp.lpSum(x[N-1][j] * (Rate[N-1][j] - 1) for j in range(N-1))

# Constraints
# Exchange Limit Constraint
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) + pulp.lpSum(x[j][i] for j in range(N)) <= Limit[i]

# Initial Currency Constraint
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= Start[i]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')