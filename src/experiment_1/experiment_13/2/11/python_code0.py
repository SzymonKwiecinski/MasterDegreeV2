import pulp

# Data from the provided JSON format
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Parameters
N = len(data['price'])
Capacity = data['capacity']
HoldingCost = data['holding_cost']
Price = data['price']
Cost = data['cost']

# Create a linear programming problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = [pulp.LpVariable(f'B_{t}', lowBound=0) for t in range(N)]  # Quantity bought
S = [pulp.LpVariable(f'S_{t}', lowBound=0) for t in range(N)]  # Quantity sold
I = [pulp.LpVariable(f'I_{t}', lowBound=0, upBound=Capacity) for t in range(N)]  # Inventory level

# Objective Function
profit_terms = [Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N)]
problem += pulp.lpSum(profit_terms)

# Constraints
# Initial inventory
problem += I[0] == 0

# Inventory balance constraints
for t in range(1, N):
    problem += I[t] == I[t-1] + B[t] - S[t]

# Non-negative inventory
for t in range(N):
    problem += I[t] >= 0
    problem += S[t] >= 0
    problem += B[t] >= 0
    problem += I[t] <= Capacity

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')