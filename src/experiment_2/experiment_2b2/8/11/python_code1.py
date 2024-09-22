import pulp

# Data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data["T"]
deliver = data["Deliver"]
storage_cost = data["StorageCost"]
switch_cost = data["SwitchCost"]

# Create a LP problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", range(T), lowBound=0, cat='Continuous')

# Objective function with absolute difference for switch cost
switch_costs = pulp.lpSum(switch_cost * abs(x[i+1] - x[i]) for i in range(T-1))
storage_costs = pulp.lpSum(storage_cost * inventory[i] for i in range(T))
problem += switch_costs + storage_costs

# Constraints
# Starting inventory
problem += inventory[0] == 0

# Inventory balance
for i in range(T):
    if i == 0:
        problem += x[i] == deliver[i] + inventory[i]
    else:
        problem += x[i] + inventory[i-1] == deliver[i] + inventory[i]

# Solve the problem
problem.solve()

# Output results
x_values = [pulp.value(x[i]) for i in range(T)]
cost = pulp.value(problem.objective)

output = {
    "x": x_values,
    "cost": cost,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')