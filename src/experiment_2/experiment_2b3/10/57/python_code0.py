import pulp

# Data parsing from JSON
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

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

# Problem definition
problem = pulp.LpProblem('Minimize_Costs', pulp.LpMinimize)

# Decision variables
amounts = pulp.LpVariable.dicts('Amount', range(T), lowBound=0, cat=pulp.LpInteger)
cranes = pulp.LpVariable.dicts('Crane', range(T), lowBound=0, upBound=num_cranes, cat=pulp.LpInteger)
end_inventory = pulp.LpVariable.dicts('EndInventory', range(T + 1), lowBound=0, upBound=max_container, cat=pulp.LpInteger)

# Objective Function
unload_cost_expression = pulp.lpSum([unload_costs[t] * amounts[t] for t in range(T)])
holding_cost_expression = holding_cost * pulp.lpSum([end_inventory[t] for t in range(T)])
crane_cost_expression = crane_cost * pulp.lpSum([cranes[t] for t in range(T)])
problem += unload_cost_expression + holding_cost_expression + crane_cost_expression

# Initial conditions
problem += end_inventory[0] == init_container

# Constraints for each month
for t in range(T):
    # Demand satisfaction
    problem += amounts[t] + end_inventory[t] >= demands[t] + end_inventory[t + 1]
    
    # Unloading capacity
    problem += amounts[t] <= unload_capacity[t]
    
    # Crane loading capacity
    problem += demands[t] <= cranes[t] * crane_capacity

# End inventory constraint for the last month
problem += end_inventory[T] == 0

# Solve the problem
problem.solve()

# Collect results
containers_unloaded = [pulp.value(amounts[t]) for t in range(T)]
cranes_rented = [pulp.value(cranes[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')