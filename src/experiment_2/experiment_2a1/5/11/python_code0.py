import pulp
import json

# Input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Define the problem
problem = pulp.LpProblem("Production_and_Inventory_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective function
total_cost = pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
             pulp.lpSum(switch_cost * abs(x[i] - x[i + 1]) for i in range(T - 1)) + \
             pulp.lpSum(x[i] for i in range(T))  # Total production cost
problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] + inventory[i] == deliver[i], f"Balance_Constr_{i}"
    else:
        problem += x[i] + inventory[i] == deliver[i] + inventory[i - 1], f"Balance_Constr_{i}"

# Solve the problem
problem.solve()

# Prepare output
solution = {
    "x": [x[i].varValue for i in range(T)],
    "cost": pulp.value(problem.objective)
}

# Print output
print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')