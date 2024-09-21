import pulp

# Data from the provided JSON format
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])  # Number of periods

# Create the problem variable
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision variables
B = pulp.LpVariable.dicts("Buy", range(N), lowBound=0)  # Quantity bought
S = pulp.LpVariable.dicts("Sell", range(N), lowBound=0)  # Quantity sold
I = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0, upBound=data['capacity'])  # Inventory level

# Objective function
problem += pulp.lpSum(data['price'][t] * S[t] - data['cost'][t] * B[t] - data['holding_cost'] * I[t] for t in range(N))

# Constraints
for t in range(N):
    # Non-negativity of inventory, sales, and purchases
    problem += I[t] >= 0  # Inventory should be non-negative
    problem += S[t] >= 0  # Sales should be non-negative
    problem += B[t] >= 0  # Purchases should be non-negative

    # Capacity constraint
    problem += I[t] <= data['capacity']  # Inventory should not exceed capacity

    # Inventory balance constraint
    if t == 0:
        problem += I[t] == 0 + B[t] - S[t]  # Initial inventory
    else:
        problem += I[t] == I[t-1] + B[t] - S[t]  # Inventory balance equation

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')