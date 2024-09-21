import pulp

# Data
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

N = len(data['price'])

# Create the problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision variables
B = [pulp.LpVariable(f'B_{t}', lowBound=0, cat='Continuous') for t in range(N)]  # Buy quantities
S = [pulp.LpVariable(f'S_{t}', lowBound=0, cat='Continuous') for t in range(N)]  # Sell quantities
I = [pulp.LpVariable(f'I_{t}', lowBound=0, cat='Continuous') for t in range(N)]  # Inventory levels

# Objective function
profit = pulp.lpSum(data['price'][t] * S[t] - data['cost'][t] * B[t] - data['holding_cost'] * I[t] for t in range(N))
problem += profit, "Total_Profit"

# Constraints
# Initial inventory
problem += (I[0] == 0, "Initial_Inventory")

# Inventory balance and capacity constraints
for t in range(N):
    if t > 0:
        problem += (I[t] == I[t-1] + B[t] - S[t], f"Inventory_Balance_{t}")
    problem += (I[t] <= data['capacity'], f"Storage_Capacity_{t}")  # Storage capacity
    problem += (S[t] >= 0, f"Non_Negative_Sales_{t}")  # Non-negative sales
    problem += (B[t] >= 0, f"Non_Negative_Purchases_{t}")  # Non-negative purchases
    problem += (I[t] >= 0, f"Non_Negative_Inventory_{t}")  # Non-negative inventory

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')