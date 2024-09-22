import pulp

# Data provided
data = {
    'N': 3,
    'Start': [100.0, 50.0, 200.0],
    'Limit': [1000.0, 200.0, 3000.0],
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

# Initialize the problem
problem = pulp.LpProblem("Currency_Exchange_Maximization", pulp.LpMaximize)

# Variables
x = pulp.LpVariable.dicts("x",
                          [(i, j) for i in range(data['N']) for j in range(data['N'])],
                          lowBound=0, cat='Continuous')

# Objective Function
problem += x[(2, 2)] + pulp.lpSum(x[(2, j)] for j in range(data['N'])), "Objective"

# Constraints

# 1. Exchange Limits
for i in range(data['N']):
    problem += pulp.lpSum(x[(i, j)] for j in range(data['N'])) <= data['Limit'][i], f"Limit_{i}"

# 2. Initial Currency Availability
for i in range(data['N']):
    for j in range(data['N']):
        problem += x[(i, j)] <= data['Start'][i], f"Start_{i}_{j}"

# 4. Exchange Rates Compliance
for i in range(data['N']):
    for j in range(data['N']):
        for k in range(data['N']):
            if i != j and j != k:  # Ensure valid sequence
                problem += x[(i, j)] * data['Rate'][i][j] <= x[(j, k)], f"Rate_{i}_{j}_{k}"

# 5. Wealth Preservation Across Cycles
# This is a complex constraint typically used to prevent arbitrage
for i in range(data['N']):
    problem += data['Rate'][i][(i+1) % data['N']] * \
               data['Rate'][(i+1) % data['N']][(i+2) % data['N']] * \
               data['Rate'][(i+2) % data['N']][i] <= 1, f"Wealth_Preservation_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')