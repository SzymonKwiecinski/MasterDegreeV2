import pulp

# Parse the input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Initialize the problem
problem = pulp.LpProblem("Production_Inventory_Optimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(T)]
inventory = [pulp.LpVariable(f'inventory_{i}', lowBound=0, cat='Continuous') for i in range(T)]

# Objective function: Minimize storage costs and switch costs
problem += pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
           pulp.lpSum(switch_cost * pulp.lpAbs(x[i+1] - x[i]) for i in range(T-1))

# Constraints
problem += (inventory[0] == x[0] - deliver[0])  # Initial inventory balance
for i in range(1, T):
    problem += (inventory[i] == inventory[i-1] + x[i] - deliver[i])  # Inventory balance for each month

# Solve the problem
problem.solve()

# Prepare output
output = {
    "x": [pulp.value(x[i]) for i in range(T)],
    "cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')