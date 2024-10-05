import pulp

# Data from the provided JSON
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

# Number of currencies
N = data['N']

# Initial amounts of each currency
start = data['Start']

# Limit amounts for exchanges
limit = data['Limit']

# Exchange rates
rate = data['Rate']

# Problem definition
problem = pulp.LpProblem("Currency_Exchange_Maximization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)),
                          lowBound=0, cat='Continuous')

# Objective function: Maximize the total amount of currency N
problem += pulp.lpSum(x[N-1, j] for j in range(N)), "Maximize_Currency_N"

# Constraints

# Currency Exchange Limits
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= limit[i], f"Limit_Currency_{i}"

# Initial Amounts constraints
for i in range(N):
    problem += start[i] - pulp.lpSum(x[i, j] for j in range(N)) + pulp.lpSum(x[j, i] for j in range(N)) >= 0, f"Initial_Amounts_{i}"

# Exchange Rate Constraints
for i in range(N):
    for j in range(N):
        problem += x[i, j] <= start[i] * rate[i][j], f"Rate_Constraint_{i}_{j}"

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')