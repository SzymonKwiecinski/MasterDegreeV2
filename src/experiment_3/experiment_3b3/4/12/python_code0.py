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

# Create the problem
problem = pulp.LpProblem("Maximize_Currency_N", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0, cat='Continuous')

# Add constraints for currency limits
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= limit[i], f"Limit_constraint_{i}"

# Objective function
final_amount = [pulp.LpVariable(f"final_amount_{i}", lowBound=0, cat='Continuous') for i in range(N)]

# Calculate the final amount of each currency
for i in range(N):
    problem += final_amount[i] == start[i] + pulp.lpSum(x[j, i] for j in range(N)) - pulp.lpSum(x[i, j] for j in range(N)), f"Final_amount_constraint_{i}"

# Constraint for exchange rates
for i in range(N):
    for j in range(N):
        if i != j:  # Avoid self-loop constraint where i == j
            problem += x[i, j] <= rate[i][j] * final_amount[i], f"Rate_constraint_{i}_{j}"

# Objective function
problem += final_amount[N-1], "Maximize_currency_N"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')