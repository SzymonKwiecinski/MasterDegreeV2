import pulp

# Data
data = {
    'T': 12, 
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
    'StorageCost': 5, 
    'SwitchCost': 10
}

# Variables
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create a LP Minimization problem
problem = pulp.LpProblem("Production_and_Inventory_Problem", pulp.LpMinimize)

# Create variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(T)]
inventory = [pulp.LpVariable(f'inv_{i}', lowBound=0, cat='Continuous') for i in range(T)]
switch = [pulp.LpVariable(f'switch_{i}', lowBound=0, cat='Continuous') for i in range(T-1)]

# Objective function
problem += (pulp.lpSum(storage_cost * inventory[i] for i in range(T))
            + pulp.lpSum(switch_cost * switch[i] for i in range(T-1)), "Total Cost")

# Constraints
# Initial inventory is zero
problem += inventory[0] == (x[0] - deliver[0])

for i in range(1, T):
    # Inventory balance constraints
    problem += inventory[i] == (inventory[i-1] + x[i] - deliver[i])

for i in range(T-1):
    # Switch constraints to handle absolute value
    problem += switch[i] >= x[i+1] - x[i]
    problem += switch[i] >= x[i] - x[i+1]

# Solve the problem
problem.solve()

# Results
results = {
    "x": [pulp.value(x[i]) for i in range(T)],
    "cost": pulp.value(problem.objective)
}

print(f'Production Plan: {results}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')