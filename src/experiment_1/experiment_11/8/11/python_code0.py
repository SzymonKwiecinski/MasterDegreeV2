import pulp
import json

# Data provided in JSON format
data = json.loads('{"capacity": 10, "holding_cost": 2, "price": [1, 2, 100], "cost": [100, 1, 100]}')

# Extracting data
capacity = data['capacity']
holding_cost = data['holding_cost']
price = data['price']
cost = data['cost']
N = len(price)  # Number of periods

# Define the problem
problem = pulp.LpProblem("Optimal_Trading_Strategy", pulp.LpMaximize)

# Decision Variables
B = pulp.LpVariable.dicts("B", range(N), lowBound=0)  # Quantity bought
S = pulp.LpVariable.dicts("S", range(N), lowBound=0)  # Quantity sold
I = pulp.LpVariable.dicts("I", range(N), lowBound=0, upBound=capacity)  # Inventory levels

# Objective Function
problem += pulp.lpSum(price[t] * S[t] - cost[t] * B[t] - holding_cost * I[t] for t in range(N))

# Constraints
# Non-negativity constraints are inherently covered by lowBound=0 in the variables
for t in range(N):
    problem += I[t] >= 0  # Non-negative inventory
    problem += S[t] >= 0  # Non-negative sales
    problem += B[t] >= 0  # Non-negative purchases
    problem += I[t] <= capacity  # Storage capacity

# Inventory balance equations
for t in range(1, N):
    problem += I[t] == I[t-1] + B[t] - S[t]  # Inventory balance

# Initial inventory
problem += I[0] == 0  # Initial inventory is zero

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')