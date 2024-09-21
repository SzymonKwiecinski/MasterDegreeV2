import pulp
import json

# Given data
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

# Parameters
N = len(data['price'])  # Number of periods
capacity = data['capacity']
holding_cost = data['holding_cost']
prices = data['price']
costs = data['cost']

# Create a linear programming problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("B", range(N), lowBound=0)  # Purchases
S = pulp.LpVariable.dicts("S", range(N), lowBound=0)  # Sales
I = pulp.LpVariable.dicts("I", range(N), lowBound=0, upBound=capacity)  # Inventory

# Objective Function
problem += pulp.lpSum([prices[t] * S[t] - costs[t] * B[t] - holding_cost * I[t] for t in range(N)])

# Constraints
for t in range(N):
    # Non-negativity constraints already handled by lowBound=0
    
    # Inventory balance
    if t == 0:
        problem += I[t] == B[t] - S[t], f"Inventory_Balance_{t}"
    else:
        problem += I[t] == I[t-1] + B[t] - S[t], f"Inventory_Balance_{t}"

    # Storage capacity constraint
    problem += I[t] <= capacity, f"Storage_Capacity_{t}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')