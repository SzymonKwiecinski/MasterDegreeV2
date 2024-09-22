import pulp

# Data
data = {
    'N': 3, 
    'Start': [100.0, 50.0, 200.0], 
    'Limit': [1000.0, 200.0, 3000.0], 
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Problem
problem = pulp.LpProblem("Maximize_Currency", pulp.LpMaximize)

# Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0, cat='Continuous')

# Objective Function
problem += x[N-1, N-1] + pulp.lpSum(x[k, N-1] for k in range(N-1)), "Objective"

# Constraints
for i in range(N):
    # Currency exchange limits
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= limit[i], f"Limit_{i}"

    # Currency available for exchange
    for j in range(N):
        problem += x[i, j] <= start[i], f"StartConstraint_{i}_{j}"

    # Conservation of currency
    problem += start[i] + pulp.lpSum(x[j, i] for j in range(N)) - pulp.lpSum(x[i, j] for j in range(N)) == (start[i] if i < N-1 else pulpLpVariable(f"final_{N}")), f"Conservation_{i}"

# Exchange rates
for i in range(N):
    for j in range(N):
        if i != j:
            problem += x[i, j] * rate[i][j] <= x[j, i], f"RateConstraint_{i}_{j}"

# Solve the problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')