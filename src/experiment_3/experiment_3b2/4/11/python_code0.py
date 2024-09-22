import pulp
import json

# Given data
data = json.loads('{"T": 12, "Deliver": [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], "StorageCost": 5, "SwitchCost": 10}')
T = data['T']
deliveries = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0)
I = pulp.LpVariable.dicts("I", range(1, T + 1), lowBound=0)
switch_vars = pulp.LpVariable.dicts("switch", range(1, T), lowBound=0)

# Objective function
problem += pulp.lpSum(storage_cost * I[i] for i in range(1, T + 1)) + \
           pulp.lpSum(switch_cost * switch_vars[i] for i in range(1, T)), "Total_Cost"

# Constraints
problem += I[1] == x[1] - deliveries[0], "Initial_Inventory_1"
for i in range(2, T + 1):
    problem += I[i] == I[i - 1] + x[i] - deliveries[i - 1], f"Inventory_Balance_{i}"

for i in range(1, T):
    problem += switch_vars[i] >= x[i + 1] - x[i], f"Switch_Positive_{i}"
    problem += switch_vars[i] >= -(x[i + 1] - x[i]), f"Switch_Negative_{i}"

for i in range(1, T + 1):
    problem += I[i] >= 0, f"Non_Negative_Inventory_{i}"

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')