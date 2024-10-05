import pulp

# Data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Problem
problem = pulp.LpProblem("Production_Inventory", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", range(T), lowBound=0, cat='Continuous')

# Objective Function
total_cost = pulp.lpSum([storage_cost * inventory[i] for i in range(T)]) + \
             pulp.lpSum([switch_cost * abs(x[i+1] - x[i]) for i in range(T-1)])
problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] - deliver[i] == inventory[i]  # Initial inventory constraint
    else:
        problem += inventory[i-1] + x[i] - deliver[i] == inventory[i]  # Inventory balance

# Solve
problem.solve()

# Output result
x_values = [pulp.value(x[i]) for i in range(T)]
cost = pulp.value(problem.objective)

output = {
    "x": x_values,
    "cost": cost,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')