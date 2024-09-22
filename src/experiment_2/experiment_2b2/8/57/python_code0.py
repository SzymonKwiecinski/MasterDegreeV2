import pulp

# Data from the problem description
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 
        'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Extracting data
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
problem = pulp.LpProblem("Seaport_Operations", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", list(range(T)), lowBound=0, cat='Integer')
cranes = pulp.LpVariable.dicts("cranes", list(range(T)), lowBound=0, upBound=num_cranes, cat='Integer')
end_inventory = pulp.LpVariable.dicts("end_inventory", list(range(T+1)), lowBound=0, upBound=max_container, cat='Integer')

# Initial condition
end_inventory[-1] = init_container

# Objective function
problem += pulp.lpSum([unload_costs[t] * amount[t] + crane_cost * cranes[t] + holding_cost * end_inventory[t] for t in range(T)])

# Constraints
for t in range(T):
    # Unloading capacity constraint
    problem += amount[t] <= unload_capacity[t], f"Unloading_Capacity_Constraint_{t}"
    # Demand fulfillment constraint
    problem += end_inventory[t-1] + amount[t] == demands[t] + end_inventory[t], f"Demand_Fulfillment_Constraint_{t}"
    # Cranes constraint
    problem += cranes[t] * crane_capacity >= demands[t], f"Cranes_Constraint_{t}"

# Final month inventory should be zero
problem += end_inventory[T-1] == 0, "Final_Inventory_Constraint"

# Solve the problem
problem.solve()

# Prepare output
containers_unloaded = [pulp.value(amount[t]) for t in range(T)]
cranes_rented = [pulp.value(cranes[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')