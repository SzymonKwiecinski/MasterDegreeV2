import pulp
import json

# Input Data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
        'CoalCost': 10, 'NukeCost': 5, 
        'MaxNuke': 20, 
        'CoalLife': 5, 'NukeLife': 10}

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the LP problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal_added = pulp.LpVariable.dicts("CoalAdded", range(T), lowBound=0, cat='Continuous')
nuke_added = pulp.LpVariable.dicts("NukeAdded", range(T), lowBound=0, cat='Continuous')

# Objective Function: Minimize total cost
problem += pulp.lpSum(coal_cost * coal_added[t] + nuke_cost * nuke_added[t] for t in range(T))

# Constraints
for t in range(T):
    total_capacity = oil_cap[t]
    # Add capacities from previous years considering their lifetime
    for c in range(1, coal_life + 1):
        if t - c >= 0:
            total_capacity += coal_added[t - c]
    for n in range(1, nuke_life + 1):
        if t - n >= 0:
            total_capacity += nuke_added[t - n]
    
    # Demand constraints
    problem += (total_capacity >= demand[t], f"Demand_Constraint_{t}")
    
    # Max nuclear capacity constraint
    problem += (nuke_added[t] <= max_nuke * total_capacity, f"Max_Nuclear_Capacity_Constraint_{t}")

# Solve the problem
problem.solve()

# Prepare the output
coal_cap_added = [pulp.value(coal_added[t]) for t in range(T)]
nuke_cap_added = [pulp.value(nuke_added[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

# Output result
result = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost
}

print(result)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')