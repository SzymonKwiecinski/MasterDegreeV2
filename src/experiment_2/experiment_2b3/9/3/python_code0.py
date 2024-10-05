import pulp

# Extracting data from JSON
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

# Define problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision variables
coal_cap_added = [pulp.LpVariable(f'CoalCapAdded_{t}', lowBound=0, cat='Continuous') for t in range(data['T'])]
nuke_cap_added = [pulp.LpVariable(f'NukeCapAdded_{t}', lowBound=0, cat='Continuous') for t in range(data['T'])]

# Objective function: Minimize total cost
total_cost = pulp.lpSum([data['CoalCost'] * coal_cap_added[t] + data['NukeCost'] * nuke_cap_added[t] for t in range(data['T'])])
problem += total_cost

# Constraints

# Capacity constraints: Coal plants last for `coal_life` years and nuclear plants for `nuke_life` years
for t in range(data['T']):
    total_coal_cap = pulp.lpSum([coal_cap_added[i] for i in range(max(0, t - data['CoalLife'] + 1), t + 1)])
    total_nuke_cap = pulp.lpSum([nuke_cap_added[i] for i in range(max(0, t - data['NukeLife'] + 1), t + 1)])
    
    problem += total_coal_cap + total_nuke_cap + data['OilCap'][t] >= data['Demand'][t]

    # Constraint on maximum nuclear capacity
    problem += total_nuke_cap <= data['MaxNuke'] / 100.0 * (data['OilCap'][t] + total_coal_cap + total_nuke_cap)

# Solve the problem
problem.solve()

# Prepare results
result = {
    "coal_cap_added": [pulp.value(coal_cap_added[t]) for t in range(data['T'])],
    "nuke_cap_added": [pulp.value(nuke_cap_added[t]) for t in range(data['T'])],
    "total_cost": pulp.value(problem.objective)
}

# Print result
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')