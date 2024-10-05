import pulp

# Data from JSON
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

# Indices
T = data['T']

# Create the Linear Programming problem
problem = pulp.LpProblem("Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal_add = pulp.LpVariable.dicts("coal_add", range(1, T + 1), lowBound=0, cat='Continuous')
nuke_add = pulp.LpVariable.dicts("nuke_add", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([data['CoalCost'] * coal_add[t] + data['NukeCost'] * nuke_add[t] for t in range(1, T + 1)])

# Constraints
for t in range(1, T + 1):
    coal_accum = pulp.lpSum(coal_add[tau] for tau in range(max(1, t - data['CoalLife'] + 1), t + 1))
    nuke_accum = pulp.lpSum(nuke_add[tau] for tau in range(max(1, t - data['NukeLife'] + 1), t + 1))

    # Demand Satisfaction
    problem += (coal_accum + nuke_accum + data['OilCap'][t - 1] >= data['Demand'][t - 1])

    # Nuclear Capacity Limit
    problem += (nuke_accum <= data['MaxNuke'] / 100 * (coal_accum + nuke_accum + data['OilCap'][t - 1]))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')