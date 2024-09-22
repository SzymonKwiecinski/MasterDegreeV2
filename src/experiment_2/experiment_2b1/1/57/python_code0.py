import pulp
import json

data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 
        'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Extracting the data from the input
T = data['T']
demands = data['Demands']
unload_costs = data['UnloadCosts']
unload_capacity = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

# Create the problem
problem = pulp.LpProblem("Seaport_Optimization", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", (t for t in range(T)), lowBound=0, cat='Integer')
cranes = pulp.LpVariable.dicts("cranes", (t for t in range(T)), lowBound=0, upBound=num_cranes, cat='Integer')
holding = pulp.LpVariable.dicts("holding", (t for t in range(T)), lowBound=0, cat='Integer')

# Objective Function
total_cost = pulp.lpSum(unload_costs[t] * amount[t] for t in range(T)) + \
             pulp.lpSum(holding_cost * holding[t] for t in range(T)) + \
             pulp.lpSum(crane_cost * cranes[t] for t in range(T))

problem += total_cost

# Constraints
# Demand fulfillment constraints
for t in range(T):
    if t == 0:
        problem += amount[t] + init_container - demands[t] + holding[t] == 0
    else:
        problem += amount[t] + holding[t-1] - demands[t] + holding[t] == 0

# Unloading constraints
for t in range(T):
    problem += amount[t] <= unload_capacity[t]

# Crane loading constraints
for t in range(T):
    problem += cranes[t] * crane_capacity >= demands[t]

# Holding constraints
for t in range(T):
    problem += holding[t] <= max_container

# Solve the problem
problem.solve()

# Results
containers_unloaded = [amount[t].varValue for t in range(T)]
cranes_rented = [cranes[t].varValue for t in range(T)]
total_cost_value = pulp.value(problem.objective)

# Output
output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')