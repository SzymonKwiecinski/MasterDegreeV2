import pulp

# Parse the given data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Define the Linear Programming problem
problem = pulp.LpProblem("Production_and_Inventory_Scheduling", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(1, T+1), lowBound=0, cat=pulp.LpContinuous)
i = pulp.LpVariable.dicts("Inventory", range(1, T+1), lowBound=0, cat=pulp.LpContinuous)

# Objective function: Minimize total cost (storage cost + switching cost)
storage_cost_expr = pulp.lpSum(storage_cost * i[month] for month in range(1, T+1))
switch_cost_expr = pulp.lpSum(switch_cost * abs(x[month+1] - x[month]) for month in range(1, T) if month < T)
problem += storage_cost_expr + switch_cost_expr

# Constraints
# Inventory balance constraints
for month in range(1, T+1):
    if month == 1:
        problem += x[month] - deliver[month-1] == i[month]
    else:
        problem += x[month] + i[month-1] - deliver[month-1] == i[month]

# Solve the problem
problem.solve()

# Results
x_values = [pulp.value(x[month]) for month in range(1, T+1)]
total_cost = pulp.value(problem.objective)

# Print results
result = {
    "x": x_values,
    "cost": total_cost,
}
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')