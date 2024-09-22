import json
import pulp

# Input data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
        'CoalCost': 10, 
        'NukeCost': 5, 
        'MaxNuke': 20, 
        'CoalLife': 5, 
        'NukeLife': 10}

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision variables
coal_capacity_added = pulp.LpVariable.dicts("Coal", range(data['T']), lowBound=0, cat='Continuous')
nuke_capacity_added = pulp.LpVariable.dicts("Nuke", range(data['T']), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['CoalCost'] * coal_capacity_added[t] + data['NukeCost'] * nuke_capacity_added[t] for t in range(data['T']))

# Constraints
for t in range(data['T']):
    total_capacity = data['OilCap'][t]
    for k in range(data['CoalLife']):
        if t - k >= 0:
            total_capacity += coal_capacity_added[t - k]
    for k in range(data['NukeLife']):
        if t - k >= 0:
            total_capacity += nuke_capacity_added[t - k]
    
    # Capacity must meet demand
    problem += total_capacity >= data['Demand'][t], f"Demand_Constraint_{t}"

# Nuclear capacity constraint
for t in range(data['T']):
    total_nuke_capacity = pulp.lpSum(nuke_capacity_added[i] for i in range(t + 1) if i < data['NukeLife'])  # Sum of nuclear capacity added
    total_capacity = data['OilCap'][t]
    for k in range(data['CoalLife']):
        if t - k >= 0:
            total_capacity += coal_capacity_added[t - k]
    
    problem += total_nuke_capacity <= (total_capacity * data['MaxNuke'] / 100), f"Nuclear_Capacity_Constraint_{t}"

# Solve the problem
problem.solve()

# Prepare the output
coal_cap_added = [coal_capacity_added[t].value() for t in range(data['T'])]
nuke_cap_added = [nuke_capacity_added[t].value() for t in range(data['T'])]
total_cost = pulp.value(problem.objective)

# Output result
result = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost,
}

print(result)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')