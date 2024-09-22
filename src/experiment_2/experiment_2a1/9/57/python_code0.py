import pulp
import json

# Input Data
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 
        'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

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

# Define the problem
problem = pulp.LpProblem("Container_Management", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Integer')
cranes = pulp.LpVariable.dicts("cranes", range(T), lowBound=0, upBound=num_cranes, cat='Integer')
inventory = pulp.LpVariable.dicts("inventory", range(T), lowBound=0, upBound=max_container, cat='Integer')

# Objective Function: Minimize total costs
total_cost = pulp.lpSum([
    unload_costs[t] * amount[t] for t in range(T)
]) + pulp.lpSum([
    holding_cost * inventory[t] for t in range(T)
]) + pulp.lpSum([
    crane_cost * cranes[t] for t in range(T)
])

problem += total_cost

# Constraints
for t in range(T):
    if t == 0:
        problem += inventory[t] == init_container + amount[t] - demands[t], f"Inventory_Constraint_{t}"
    else:
        problem += inventory[t] == inventory[t-1] + amount[t] - demands[t], f"Inventory_Constraint_{t}"
    
    problem += amount[t] <= unload_capacity[t], f"Unload_Capacity_Constraint_{t}"
    problem += amount[t] <= max_container - inventory[t-1] if t > 0 else amount[t] <= max_container - init_container, f"Max_Container_Constraint_{t}"
    
    # Crane usage constraint
    problem += cranes[t] * crane_capacity >= demands[t] - (inventory[t-1] if t > 0 else init_container), f"Cranes_Capacity_Constraint_{t}"

# Final inventory should be zero
problem += inventory[T-1] == 0, "Final_Inventory_Constraint"

# Solve the problem
problem.solve()

# Prepare output
containers_unloaded = [int(amount[t].varValue) for t in range(T)]
cranes_rented = [int(cranes[t].varValue) for t in range(T)]
total_cost_value = pulp.value(problem.objective)

output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

# Print Object Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')