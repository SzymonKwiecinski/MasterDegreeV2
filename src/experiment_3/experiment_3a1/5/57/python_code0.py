import pulp

# Data from JSON
data = {
    'T': 4,
    'Demands': [450, 700, 500, 750],
    'UnloadCosts': [75, 100, 105, 130],
    'UnloadCapacity': [800, 500, 450, 700],
    'HoldingCost': 20,
    'MaxContainer': 500,
    'InitContainer': 200,
    'NumCranes': 4,
    'CraneCapacity': 200,
    'CraneCost': 1000
}

# Create the problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0, cat='Continuous') for t in range(data['T'])]
crane = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=data['NumCranes'], cat='Integer') for t in range(data['T'])]
inventory = [pulp.LpVariable(f'inventory_{t}', lowBound=0, cat='Continuous') for t in range(data['T'] + 1)]

# Objective Function
total_cost = pulp.lpSum([
    data['UnloadCosts'][t] * amount[t] +
    data['HoldingCost'] * inventory[t] +
    data['CraneCost'] * crane[t] for t in range(data['T'])
])
problem += total_cost

# Constraints
# Capacity Constraint
for t in range(data['T']):
    problem += amount[t] <= data['UnloadCapacity'][t]

# Demand Fulfillment and Inventory Constraints
for t in range(data['T']):
    if t == 0:
        problem += inventory[t] == data['InitContainer'] + amount[t] - data['Demands'][t]
    else:
        problem += inventory[t] == inventory[t-1] + amount[t] - data['Demands'][t]

# Final Inventory Constraint
problem += inventory[data['T']] == 0

# Storage Capacity Constraint
for t in range(data['T']):
    problem += inventory[t] <= data['MaxContainer']

# Cranes Usage Constraint
for t in range(data['T']):
    problem += crane[t] * data['CraneCapacity'] >= amount[t]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')