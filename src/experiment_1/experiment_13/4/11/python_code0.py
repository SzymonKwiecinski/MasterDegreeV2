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

# Create the linear programming problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("Buy", range(N), lowBound=0)  # Quantity bought
S = pulp.LpVariable.dicts("Sell", range(N), lowBound=0)  # Quantity sold
I = pulp.LpVariable.dicts("Inventory", range(N), lowBound=0, upBound=Capacity)  # Inventory levels

# Objective Function
problem += pulp.lpSum(Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N)), "Total_Profit"

# Constraints
# Non-negative inventory
for t in range(N):
    problem += I[t] >= 0, f"NonNegativeInventory_{t}"

# Non-negative sales
for t in range(N):
    problem += S[t] >= 0, f"NonNegativeSales_{t}"

# Non-negative purchases
for t in range(N):
    problem += B[t] >= 0, f"NonNegativePurchases_{t}"

# Storage capacity
for t in range(N):
    problem += I[t] <= Capacity, f"StorageCapacity_{t}"

# Inventory balance
for t in range(1, N):
    problem += I[t] == I[t-1] + B[t] - S[t], f"InventoryBalance_{t}"

# Initial inventory
problem += I[0] == 0, "InitialInventory"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')