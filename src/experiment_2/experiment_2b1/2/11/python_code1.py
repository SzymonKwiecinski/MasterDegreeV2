import pulp
import json

# Given data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data['T']
deliveries = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Define the problem
problem = pulp.LpProblem("Production_and_Inventory_Cost_Minimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective function
switching_cost = pulp.lpSum(switch_cost * (x[i] - x[i + 1]) for i in range(T - 1))
total_cost = pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
              switching_cost + pulp.lpSum(x[i] for i in range(T))
              
problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] - deliveries[i] + inventory[i] == 0, f"Balance_0"
    else:
        problem += x[i] - deliveries[i] + inventory[i] - inventory[i - 1] == 0, f"Balance_{i}"

# Inventory cannot be negative
for i in range(T):
    problem += inventory[i] >= 0, f"Nonnegative_Inventory_{i}"

# Solve the problem
problem.solve()

# Gather results
x_values = [x[i].varValue for i in range(T)]
cost = pulp.value(problem.objective)

# Output results
output = {
    "x": x_values,
    "cost": cost,
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')