import pulp
import json

# Input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

# Extracting data
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create a LP problem
problem = pulp.LpProblem("Production_Inventory_Cost_Minimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective function: minimize total costs
total_cost = pulp.lpSum(storage_cost * inventory[i] for i in range(T)) + \
              pulp.lpSum(switch_cost * abs(x[i+1] - x[i]) for i in range(T - 1)) + \
              pulp.lpSum(x[i] for i in range(T))  # add production cost, if any
              
problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] - deliver[i] + inventory[i] == 0  # for the first month
    else:
        problem += x[i] - deliver[i] + inventory[i] == inventory[i-1]  # inventory carries over

# Solve the problem
problem.solve()

# Collect results
result_x = [x[i].varValue for i in range(T)]
cost = pulp.value(problem.objective)

# Output data
output = {
    "x": result_x,
    "cost": cost,
}

# Printing the result
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{cost}</OBJ>')