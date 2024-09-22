import json
import pulp

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
max_nuke = data['MaxNuke'] / 100
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision variables
coal_added = [pulp.LpVariable(f'coal_added_{t}', lowBound=0) for t in range(T)]
nuke_added = [pulp.LpVariable(f'nuke_added_{t}', lowBound=0) for t in range(T)]

# Objective function
total_cost = pulp.lpSum([coal_added[t] * coal_cost for t in range(T)]) + pulp.lpSum([nuke_added[t] * nuke_cost for t in range(T)])
problem += total_cost

# Constraints
for t in range(T):
    total_capacity = oil_cap[t] + pulp.lpSum([coal_added[tau] for tau in range(max(0, t - coal_life + 1), t + 1)]) + pulp.lpSum([nuke_added[tau] for tau in range(max(0, t - nuke_life + 1), t + 1)])
    problem += total_capacity >= demand[t], f'Demand_constraint_{t}'

# Nuclear capacity limit constraint
for t in range(T):
    if t >= nuke_life - 1:
        problem += pulp.lpSum([nuke_added[tau] for tau in range(max(0, t - nuke_life + 1), t + 1)]) <= (total_capacity * max_nuke), f'Nuclear_limit_{t}'

# Solve the problem
problem.solve()

# Prepare output
coal_cap_added = [coal_added[t].varValue for t in range(T)]
nuke_cap_added = [nuke_added[t].varValue for t in range(T)]
total_cost_value = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')