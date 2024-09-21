import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Number of periods
N = len(data['price'])

# Create the problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = [pulp.LpVariable(f"B_{t}", lowBound=0, cat='Continuous') for t in range(N)]
S = [pulp.LpVariable(f"S_{t}", lowBound=0, cat='Continuous') for t in range(N)]
I = [pulp.LpVariable(f"I_{t}", lowBound=0, cat='Continuous') for t in range(N)]

# Constraints
# Initial inventory
problem += (I[0] == 0)

# Inventory balance
for t in range(1, N):
    problem += (I[t] == I[t-1] + B[t] - S[t])

# Capacity constraints
for t in range(N):
    problem += (I[t] <= data['capacity'])

# Objective Function
profit_expr = sum(data['price'][t] * S[t] - data['cost'][t] * B[t] - data['holding_cost'] * I[t] for t in range(N))
problem += profit_expr

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')