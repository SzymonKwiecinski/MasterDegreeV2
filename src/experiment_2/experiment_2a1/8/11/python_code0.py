import pulp
import json

# Input data
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}

# Extracting parameters
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Initialize the problem
problem = pulp.LpProblem("Production_Inventory_Schedule", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Produce", range(T), lowBound=0, cat='Continuous')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective function
total_cost = pulp.lpSum(switch_cost * pulp.lpAbs(x[i] - x[i + 1]) for i in range(T - 1)) 
                        + pulp.lpSum(storage_cost * inventory[i] for i in range(T))

problem += total_cost

# Constraints
for i in range(T):
    if i == 0:
        problem += x[i] - deliver[i] + inventory[i] == 0  # First month
    else:
        problem += x[i] - deliver[i] + inventory[i] - inventory[i - 1] == 0  # Following months

# End of the year inventory should not incur any cost
problem += inventory[T - 1] == 0

# Solve the problem
problem.solve()

# Output results
result_x = [x[i].varValue for i in range(T)]
cost = pulp.value(problem.objective)

output = {
    "x": result_x,
    "cost": cost,
}

print(f' (Objective Value): <OBJ>{cost}</OBJ>')