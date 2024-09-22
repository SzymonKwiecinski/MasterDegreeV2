import pulp
import json

# Input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Define the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(T)]  # Production quantities
inventory = [pulp.LpVariable(f'inventory_{i}', lowBound=0, cat='Continuous') for i in range(T)]  # Inventory levels

# Objective function
total_cost = pulp.lpSum([storage_cost * inventory[i] for i in range(T)]) + \
             pulp.lpSum([switch_cost * (x[i] - x[i+1]) for i in range(T-1)]) + \
             pulp.lpSum([switch_cost * (x[i+1] - x[i]) for i in range(T-1)])
problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        problem += (x[i] - deliver[i] + inventory[i] == 0, f"Balance_Constraint_{i}")
    else:
        problem += (x[i] - deliver[i] + inventory[i] + inventory[i-1] - x[i-1] == 0, f"Balance_Constraint_{i}")
    
    if i < T - 1:
        # Enforce that inventory is carried over to the next month
        problem += (inventory[i] >= 0, f"Inventory_Nonnegativity_{i}")

# Solve the problem
problem.solve()

# Prepare output
result = {
    "x": [pulp.value(x[i]) for i in range(T)],
    "cost": pulp.value(problem.objective)
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')