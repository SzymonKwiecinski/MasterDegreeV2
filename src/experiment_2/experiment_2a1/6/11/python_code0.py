import pulp

# Input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the linear programming problem
problem = pulp.LpProblem("Production_and_Inventory_Management", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective Function
total_cost = pulp.lpSum([
    storage_cost * inventory[i] for i in range(T)
]) + pulp.lpSum([
    switch_cost * pulp.lpAbs(x[i+1] - x[i]) for i in range(T-1)
]) + pulp.lpSum([x[i] for i in range(T)])  # Production cost (implicitly 1 per unit produced)

problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] - deliver[i] + inventory[i] == 0  # First month
    else:
        problem += x[i] - deliver[i] + inventory[i] == inventory[i-1]  # Following months

# Solve the problem
problem.solve()

# Prepare the output
production = [x[i].varValue for i in range(T)]
cost = pulp.value(problem.objective)

# Output result
output = {
    "x": production,
    "cost": cost,
}

print(f' (Objective Value): <OBJ>{cost}</OBJ>')