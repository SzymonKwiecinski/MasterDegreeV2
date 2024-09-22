import pulp
import json

# Input data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
        'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 
        'CoalLife': 5, 'NukeLife': 10}

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the LP problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision variables
coal_capacity_added = pulp.LpVariable.dicts("CoalCapacity", range(T), lowBound=0, cat='Continuous')
nuke_capacity_added = pulp.LpVariable.dicts("NukeCapacity", range(T), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(coal_cost * coal_capacity_added[t] + nuke_cost * nuke_capacity_added[t] for t in range(T))

# Constraints
for t in range(T):
    # Total capacity must meet demand
    total_capacity = oil_cap[t] + pulp.lpSum(coal_capacity_added[max(0, t-i)] for i in range(1, min(coal_life, t) + 1)) + \
                     pulp.lpSum(nuke_capacity_added[max(0, t-i)] for i in range(1, min(nuke_life, t) + 1))
    problem += total_capacity >= demand[t]

# Nuclear capacity constraint
for t in range(T):
    total_nuclear_capacity = pulp.lpSum(nuke_capacity_added[max(0, t-i)] for i in range(1, min(nuke_life, t) + 1))
    total_capacity = oil_cap[t] + pulp.lpSum(coal_capacity_added[max(0, t-i)] for i in range(1, min(coal_life, t) + 1)) + total_nuclear_capacity
    problem += total_nuclear_capacity <= (max_nuke / 100) * total_capacity

# Solve the problem
problem.solve()

# Collect results
coal_cap_added = [coal_capacity_added[t].varValue for t in range(T)]
nuke_cap_added = [nuke_capacity_added[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

# Create output dictionary
output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost
}

# Print the result
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')