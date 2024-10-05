import pulp

# Data from JSON
data = {
    'T': 4,
    'Demands': [450, 700, 500, 750],
    'UnloadCosts': [75, 100, 105, 130],
    'UnloadCapacity': [800, 500, 450, 700],
    'HoldingCost': 20,
    'MaxContainer': 500,
    'InitContainer': 200,
    'NumCranes': 4,
    'CraneCapacity': 200,
    'CraneCost': 1000
}

# Initialize problem
problem = pulp.LpProblem("Minimize_Seaport_Costs", pulp.LpMinimize)

# Sets and Parameters
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

# Decision Variables
amount = pulp.LpVariable.dicts("Amount", range(1, T + 1), lowBound=0, cat=pulp.LpInteger)
cranes = pulp.LpVariable.dicts("Cranes", range(1, T + 1), lowBound=0, upBound=num_cranes, cat=pulp.LpInteger)
inventory = pulp.LpVariable.dicts("Inventory", range(0, T + 1), lowBound=0, upBound=max_container, cat=pulp.LpInteger)

# Initial inventory
problem += inventory[0] == init_container, "Initial_Inventory"

# Constraints
for t in range(1, T + 1):
    # Balance Constraint
    problem += inventory[t-1] + amount[t] - demands[t-1] == inventory[t], f"Balance_Month_{t}"
    
    # Unloading capacity constraint
    problem += amount[t] <= unload_capacity[t-1], f"Unloading_Capacity_Month_{t}"
    
    # Crane capacity constraint
    problem += demands[t-1] <= cranes[t] * crane_capacity, f"Crane_Capacity_Month_{t}"

# End inventory constraint
problem += inventory[T] == 0, "End_Inventory"

# Objective function
problem += pulp.lpSum([unload_costs[t-1] * amount[t] for t in range(1, T + 1)]) + \
           pulp.lpSum([holding_cost * inventory[t] for t in range(1, T)]) + \
           pulp.lpSum([crane_cost * cranes[t] for t in range(1, T + 1)]), "Total_Cost"

# Solve the problem
problem.solve()

# Extract solution
containers_unloaded = [int(amount[t].varValue) for t in range(1, T + 1)]
cranes_rented = [int(cranes[t].varValue) for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

# Output
output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')