import pulp

# Data from JSON
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

# Create the problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision variables
B = pulp.LpVariable.dicts("Buy", range(N), lowBound=0)  # Quantity bought
S = pulp.LpVariable.dicts("Sell", range(N), lowBound=0)  # Quantity sold
I = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0, upBound=Capacity)  # Inventory levels

# Objective function
profit = pulp.lpSum([Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N)])
problem += profit

# Constraints
for t in range(N):
    # Non-negative inventory
    problem += I[t] >= 0, f"NonNegInventory_{t}"

    # Non-negative sales
    problem += S[t] >= 0, f"NonNegSales_{t}"

    # Non-negative purchases
    problem += B[t] >= 0, f"NonNegPurchases_{t}"

    # Storage capacity
    problem += I[t] <= Capacity, f"StorageCapacity_{t}"

    # Inventory balance
    if t == 0:
        problem += I[t] == 0 + B[t] - S[t], f"InventoryBalance_{t}"  # Initial inventory
    else:
        problem += I[t] == I[t-1] + B[t] - S[t], f"InventoryBalance_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')