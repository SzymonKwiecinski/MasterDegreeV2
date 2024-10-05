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

# Extract data
N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Define the linear programming problem
problem = pulp.LpProblem("Currency_Exchange_Maximization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(x[N-1, j] for j in range(N)) 

# Constraints

# 1. Exchange limits
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= Limit[i]

# 2. Final amount constraints
for i in range(N):
    problem += Start[i] + pulp.lpSum(x[i, j] for j in range(N) if j != i) - pulp.lpSum(x[j, i] for j in range(N) if j != i) >= 0

# 4. Cycle constraints
# These are typically derived from the rates ensuring no arbitrage, but we assume proper rates given in input

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')