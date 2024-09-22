import pulp
import json

# Input data in JSON format
data = {
    'T': 12, 
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
    'CoalCost': 10, 
    'NukeCost': 5, 
    'MaxNuke': 20, 
    'CoalLife': 5, 
    'NukeLife': 10
}

# Extracting variables from the data
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the optimization problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision variables
coal_cap_added = pulp.LpVariable.dicts("CoalCapAdded", range(T), lowBound=0, cat='Continuous')
nuke_cap_added = pulp.LpVariable.dicts("NukeCapAdded", range(T), lowBound=0, cat='Continuous')

# Objective function: minimize total cost
problem += pulp.lpSum([coal_cap_added[t] * coal_cost for t in range(T)]) + pulp.lpSum([nuke_cap_added[t] * nuke_cost for t in range(T)])

# Constraints: ensuring demand is met and capacity limits
for t in range(T):
    total_capacity = oil_cap[t]
    for t_c in range(max(0, t - coal_life + 1), t + 1):
        total_capacity += coal_cap_added[t_c]
    for t_n in range(max(0, t - nuke_life + 1), t + 1):
        total_capacity += nuke_cap_added[t_n]
    
    problem += total_capacity >= demand[t], f"DemandConstraint_{t}"

# Constraint for maximum nuclear capacity
for t in range(T):
    nuke_capacity = pulp.lpSum(nuke_cap_added[t_n] for t_n in range(max(0, t - nuke_life + 1), t + 1))
    total_capacity = oil_cap[t] + pulp.lpSum(coal_cap_added[t_c] for t_c in range(max(0, t - coal_life + 1), t + 1)) + nuke_capacity
    problem += nuke_capacity <= max_nuke * total_capacity, f"NuclearConstraint_{t}"

# Solve the problem
problem.solve()

# Prepare output
coal_cap_added_values = [pulp.value(coal_cap_added[t]) for t in range(T)]
nuke_cap_added_values = [pulp.value(nuke_cap_added[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_cap_added_values,
    "nuke_cap_added": nuke_cap_added_values,
    "total_cost": total_cost,
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')