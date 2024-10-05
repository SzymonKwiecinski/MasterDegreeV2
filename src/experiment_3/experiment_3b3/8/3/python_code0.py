import pulp

# Define data
data = {
    'T': 12,
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
    'CoalCost': 10,
    'NukeCost': 5,
    'MaxNuke': 0.2,  # Converted to fraction
    'CoalLife': 5,
    'NukeLife': 10
}

# Initialize problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision variables
coal = [pulp.LpVariable(f'coal_{t}', lowBound=0) for t in range(data['T'])]
nuke = [pulp.LpVariable(f'nuke_{t}', lowBound=0) for t in range(data['T'])]

# Objective function: Minimize total cost
total_cost = pulp.lpSum(data['CoalCost'] * coal[t] + data['NukeCost'] * nuke[t] for t in range(data['T']))
problem += total_cost

# Constraints

# Demand satisfaction constraints
for t in range(data['T']):
    coal_capacity = pulp.lpSum(coal[max(0, t-j)] for j in range(min(t+1, data['CoalLife'])))
    nuke_capacity = pulp.lpSum(nuke[max(0, t-j)] for j in range(min(t+1, data['NukeLife'])))
    problem += data['OilCap'][t] + coal_capacity + nuke_capacity >= data['Demand'][t]

# Nuclear capacity constraint
total_coal_nuke_capacity = pulp.lpSum(data['OilCap'][t] + pulp.lpSum(coal[max(0, t-j)] for j in range(min(t+1, data['CoalLife']))) + pulp.lpSum(nuke[max(0, t-j)] for j in range(min(t+1, data['NukeLife']))) for t in range(data['T']))
problem += pulp.lpSum(nuke[t] for t in range(data['T'])) <= data['MaxNuke'] * total_coal_nuke_capacity

# Solve the problem
problem.solve()

# Output results
coal_cap_added = [coal[t].varValue for t in range(data['T'])]
nuke_cap_added = [nuke[t].varValue for t in range(data['T'])]
total_cost = pulp.value(problem.objective)

print(f"coal_cap_added: {coal_cap_added}")
print(f"nuke_cap_added: {nuke_cap_added}")
print(f"total_cost (Objective Value): <OBJ>{total_cost}</OBJ>")