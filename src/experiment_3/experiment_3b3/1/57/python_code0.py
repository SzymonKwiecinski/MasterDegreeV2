import pulp

# Data
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

# Indices
T = data['T']

# Create the Linear Programming problem
problem = pulp.LpProblem("Container_Handling", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("Amount", range(1, T + 1), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("Crane", range(1, T + 1), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective Function
total_cost = pulp.lpSum(
    data['UnloadCosts'][t - 1] * amount[t] + 
    data['HoldingCost'] * inventory[t] + 
    data['CraneCost'] * crane[t] 
    for t in range(1, T + 1)
)
problem += total_cost

# Constraints
# Initial Inventory
problem += inventory[1] == data['InitContainer'] + amount[1] - data['Demands'][0]

# Inventory Balance
for t in range(2, T + 1):
    problem += inventory[t] == inventory[t - 1] + amount[t] - data['Demands'][t - 1]

# Unload Capacity
for t in range(1, T + 1):
    problem += amount[t] <= data['UnloadCapacity'][t - 1]

# Demand Satisfaction
for t in range(1, T + 1):
    problem += amount[t] >= data['Demands'][t - 1]

# Inventory Limit
for t in range(1, T + 1):
    problem += inventory[t] <= data['MaxContainer']

# Crane Capacity
for t in range(1, T + 1):
    problem += crane[t] * data['CraneCapacity'] >= data['Demands'][t - 1]

# Crane Limit
for t in range(1, T + 1):
    problem += crane[t] <= data['NumCranes']

# Solve the problem
problem.solve()

# Output the results
for t in range(1, T + 1):
    print(f"Month {t}: Amount unloaded = {amount[t].varValue}, Cranes rented = {crane[t].varValue}, Inventory = {inventory[t].varValue}")

print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')