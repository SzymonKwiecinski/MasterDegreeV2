import pulp

# Given data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])  # Number of periods

# Create a linear programming problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision variables
B = pulp.LpVariable.dicts("Buy", range(N), lowBound=0)  # Quantity bought
S = pulp.LpVariable.dicts("Sell", range(N), lowBound=0)  # Quantity sold
I = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0)  # Inventory level

# Objective function
problem += pulp.lpSum(data['price'][t] * S[t] - data['cost'][t] * B[t] - data['holding_cost'] * I[t] for t in range(N))

# Constraints
# Non-negative inventory
for t in range(N):
    problem += I[t] >= 0, f"NonNegativeInventory_t{t}"

# Non-negative sales
for t in range(N):
    problem += S[t] >= 0, f"NonNegativeSales_t{t}"

# Non-negative purchases
for t in range(N):
    problem += B[t] >= 0, f"NonNegativePurchases_t{t}"

# Storage capacity
for t in range(N):
    problem += I[t] <= data['capacity'], f"StorageCapacity_t{t}"

# Inventory balance and initial inventory
for t in range(N):
    if t == 0:
        problem += I[t] == B[t] - S[t], f"InventoryBalance_t{t}"
    else:
        problem += I[t] == I[t-1] + B[t] - S[t], f"InventoryBalance_t{t}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')