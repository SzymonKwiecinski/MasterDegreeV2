import pulp
import json

# Data
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

# Parameters
N = len(data['price'])
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']

# Problem definition
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("B", range(N), lowBound=0)  # Quantity bought
S = pulp.LpVariable.dicts("S", range(N), lowBound=0)  # Quantity sold
I = pulp.LpVariable.dicts("I", range(N), lowBound=0, upBound=capacity)  # Inventory level

# Objective Function
problem += pulp.lpSum(price[t] * S[t] - cost[t] * B[t] - holding_cost * I[t] for t in range(N)), "Total_Profit"

# Constraints
# Initial inventory
problem += I[0] == 0, "Initial_Inventory"
# Inventory balance
for t in range(1, N):
    problem += I[t] == I[t-1] + B[t] - S[t], f"Inventory_Balance_{t}"
# Non-negativity and capacity constraints
for t in range(N):
    problem += I[t] >= 0, f"Non_Negative_Inventory_{t}"
    problem += S[t] >= 0, f"Non_Negative_Sales_{t}"
    problem += B[t] >= 0, f"Non_Negative_Purchases_{t}"
    problem += I[t] <= capacity, f"Storage_Capacity_{t}"

# Solve the problem
problem.solve()

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')