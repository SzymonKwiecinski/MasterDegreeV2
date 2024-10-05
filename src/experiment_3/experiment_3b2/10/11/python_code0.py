import pulp
import json

# Data
data = json.loads('{"T": 12, "Deliver": [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], "StorageCost": 5, "SwitchCost": 10}')
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Define the LP problem
problem = pulp.LpProblem("Inventory_Management", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T), lowBound=0)  # Switch amount
I = pulp.LpVariable.dicts("I", range(T), lowBound=0)  # Inventory level

# Objective function
problem += pulp.lpSum(storage_cost * I[i] + switch_cost * pulp.lpAbs(x[i] - x[i-1]) for i in range(T) if i > 0)

# Constraints
I[0] = 0  # Initial inventory is zero
for i in range(T):
    if i > 0:
        problem += I[i] == I[i-1] + x[i] - deliver[i]  # Inventory balance
    else:
        problem += I[i] == 0 + x[i] - deliver[i]  # For i = 0, I[0] = 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')