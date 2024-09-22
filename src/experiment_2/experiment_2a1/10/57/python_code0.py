import pulp
import json

data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 
        'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Unpack data
T = data['T']
demands = data['Demands']
unload_costs = data['UnloadCosts']
unload_capacities = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

# Create the problem variable
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Define decision variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0, upBound=unload_capacities[t-1], cat='Integer') for t in range(1, T+1)]
cranes = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=num_cranes, cat='Integer') for t in range(1, T+1)]
inventory = [pulp.LpVariable(f'inventory_{t}', lowBound=0, upBound=max_container, cat='Integer') for t in range(T+1)]

# Initial inventory constraint
problem += (inventory[0] == init_container)

# Inventory balance and demand fulfillment constraints
for t in range(1, T+1):
    if t < T:
        problem += (inventory[t-1] + amount[t-1] - demands[t-1] == inventory[t])
    else:
        problem += (inventory[t-1] + amount[t-1] - demands[t-1] == 0)

# Crane constraints
for t in range(1, T+1):
    problem += (cranes[t-1] * crane_capacity >= demands[t-1])

# Objective function
total_cost = pulp.lpSum(unload_costs[t-1] * amount[t-1] for t in range(1, T+1)) + \
             pulp.lpSum(holding_cost * inventory[t] for t in range(1, T+1)) + \
             pulp.lpSum(crane_cost * cranes[t-1] for t in range(1, T+1))

problem += total_cost

# Solve the problem
problem.solve()

# Prepare output
containers_unloaded = [int(amount[t].varValue) for t in range(T)]
cranes_rented = [int(cranes[t].varValue) for t in range(T)]
total_cost_value = pulp.value(problem.objective)

# Print results
output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')