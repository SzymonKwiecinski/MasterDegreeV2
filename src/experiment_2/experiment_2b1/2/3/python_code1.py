import pulp
import json

# Input data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
        'CoalCost': 10, 'NukeCost': 5, 
        'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}

# Parameters
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke_percentage = data['MaxNuke'] / 100
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Problem Definition
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal_vars = pulp.LpVariable.dicts("Coal", range(T), lowBound=0, cat='Continuous')
nuke_vars = pulp.LpVariable.dicts("Nuke", range(T), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(coal_cost * coal_vars[t] for t in range(T)) + pulp.lpSum(nuke_cost * nuke_vars[t] for t in range(T))

# Constraints
for t in range(T):
    total_capacity = oil_cap[t]
    
    # Adding coal and nuclear capacities from previous years
    if t >= coal_life:
        total_capacity += pulp.lpSum(coal_vars[t - k] for k in range(1, coal_life + 1) if t - k >= 0)
    if t >= nuke_life:
        total_capacity += pulp.lpSum(nuke_vars[t - k] for k in range(1, nuke_life + 1) if t - k >= 0)
    
    # Demand constraint
    problem += total_capacity >= demand[t], f"Demand_Constraint_{t}"

# Nuclear Capacity Constraint
for t in range(T):
    total_capacity = oil_cap[t]

    if t >= coal_life:
        total_capacity += pulp.lpSum(coal_vars[t - k] for k in range(1, coal_life + 1) if t - k >= 0)
    if t >= nuke_life:
        total_capacity += pulp.lpSum(nuke_vars[t - k] for k in range(1, nuke_life + 1) if t - k >= 0)

    # Adding the constraint for the maximum percentage of nuclear capacity
    problem += pulp.lpSum(nuke_vars[t2] for t2 in range(t + 1) if t2 < T) <= max_nuke_percentage * total_capacity, f"Nuclear_Capacity_Constraint_{t}"

# Solve the problem
problem.solve()

# Results
coal_cap_added = [coal_vars[t].varValue for t in range(T)]
nuke_cap_added = [nuke_vars[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost
}

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')