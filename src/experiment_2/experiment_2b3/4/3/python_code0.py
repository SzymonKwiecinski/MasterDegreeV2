import pulp

# Extract data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100.0
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Initialize LP Problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision Variables
coal_cap_added = [pulp.LpVariable(f'CoalCapAdded_{t}', lowBound=0) for t in range(T)]
nuke_cap_added = [pulp.LpVariable(f'NukeCapAdded_{t}', lowBound=0) for t in range(T)]

# Objective Function
total_cost = pulp.lpSum([coal_cost * coal_cap_added[t] + nuke_cost * nuke_cap_added[t] for t in range(T)])
problem += total_cost

# Constraints
for t in range(T):
    # Available capacity constraints
    available_coal = pulp.lpSum([coal_cap_added[i] for i in range(max(0, t - coal_life + 1), t + 1)])
    available_nuke = pulp.lpSum([nuke_cap_added[i] for i in range(max(0, t - nuke_life + 1), t + 1)])
    problem += (oil_cap[t] + available_coal + available_nuke >= demand[t])
    
    # Nuclear capacity percentage constraint
    problem += (available_nuke <= max_nuke * (oil_cap[t] + available_coal + available_nuke))

# Solve problem
problem.solve()

# Extract Results
coal_cap_result = [coal_cap_added[t].varValue for t in range(T)]
nuke_cap_result = [nuke_cap_added[t].varValue for t in range(T)]
total_cost_result = pulp.value(problem.objective)

# Output format
output = {
    "coal_cap_added": coal_cap_result,
    "nuke_cap_added": nuke_cap_result,
    "total_cost": total_cost_result,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')