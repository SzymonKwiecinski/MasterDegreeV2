import pulp
import json

# Input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the LP problem
problem = pulp.LpProblem("Production_Inventory_Problem", pulp.LpMinimize)

# Decision variables: production quantity for each month
x = pulp.LpVariable.dicts("x", range(T), lowBound=0, cat='Continuous')

# Inventory variables
inventory = pulp.LpVariable.dicts("inventory", range(T), lowBound=0, cat='Continuous')

# Objective function: minimize total cost
switch_cost_total = pulp.lpSum(switch_cost * (x[i+1] - x[i]) for i in range(T-1) if x[i+1] >= x[i]) + \
                                pulp.lpSum(switch_cost * (x[i] - x[i+1]) for i in range(T-1) if x[i+1] < x[i])

problem += pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
           switch_cost_total + \
           pulp.lpSum(x[i] for i in range(T)), "Total_Cost"

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] - deliver[i] + inventory[i] == 0, f"Balance_Month_{i+1}"
    else:
        problem += x[i] + inventory[i-1] - deliver[i] + inventory[i] == 0, f"Balance_Month_{i+1}"

# Solve the problem
problem.solve()

# Collect results
result_x = [x[i].varValue for i in range(T)]
cost = pulp.value(problem.objective)

# Output format
output = {
    "x": result_x,
    "cost": cost,
}

print(output)
print(f' (Objective Value): <OBJ>{cost}</OBJ>')