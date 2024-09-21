import pulp

# Data from the JSON input
data = {
    'capacity': 10,
    'holding_cost': 2,
    'price': [1, 2, 100],
    'cost': [100, 1, 100]
}

# Parameters
N = len(data['price'])  # Number of periods
Capacity = data['capacity']
HoldingCost = data['holding_cost']
Price = data['price']
Cost = data['cost']

# Create the problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("B", range(N), lowBound=0)  # Bought
S = pulp.LpVariable.dicts("S", range(N), lowBound=0)  # Sold
I = pulp.LpVariable.dicts("I", range(N), lowBound=0, upBound=Capacity)  # Inventory

# Objective Function
profit = pulp.lpSum(Price[t] * S[t] - Cost[t] * B[t] - HoldingCost * I[t] for t in range(N))
problem += profit, "Total_Profit"

# Constraints
# Initial inventory
problem += I[0] == 0, "Initial_Inventory"

# Inventory balance and constraints
for t in range(N):
    if t > 0:
        problem += I[t] == I[t-1] + B[t] - S[t], f"Inventory_Balance_{t}"
    problem += I[t] >= 0, f"Non_Negative_Inventory_{t}"
    problem += S[t] >= 0, f"Non_Negative_Sales_{t}"
    problem += B[t] >= 0, f"Non_Negative_Purchases_{t}"
    problem += I[t] <= Capacity, f"Storage_Capacity_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')