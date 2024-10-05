import pulp

# Data
data = {
    'N': 3,
    'Start': [100.0, 50.0, 200.0],
    'Limit': [1000.0, 200.0, 3000.0],
    'Rate': [
        [0.99, 0.9, 1.02],
        [0.95, 0.99, 0.92],
        [0.9, 0.91, 0.99]
    ]
}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Initialize the problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0)

# Objective Function
objective = (
    pulp.lpSum(x[i, N-1] * rate[i][N-1] for i in range(N-1)) +
    start[N-1] +
    pulp.lpSum(x[N-1, j] * rate[N-1][j] for j in range(N-1))
)
problem += objective

# Constraints

# Currency Start Constraint
for i in range(N):
    problem += (
        pulp.lpSum(x[j, i] * rate[j][i] for j in range(N)) +
        start[i] -
        pulp.lpSum(x[i, k] for k in range(N)) <= start[i]
    )

# Exchange Limit Constraint
for i in range(N):
    problem += (pulp.lpSum(x[i, j] for j in range(N)) <= limit[i])

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')