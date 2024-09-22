import pulp

# Data
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

# Problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal_added = [pulp.LpVariable(f"coal_added_{t}", lowBound=0, cat='Continuous') for t in range(data['T'])]
nuke_added = [pulp.LpVariable(f"nuke_added_{t}", lowBound=0, cat='Continuous') for t in range(data['T'])]

# Objective Function
problem += pulp.lpSum(data['CoalCost'] * coal_added[t] + data['NukeCost'] * nuke_added[t] for t in range(data['T']))

# Constraints
for t in range(data['T']):
    coal_lifetime_sum = pulp.lpSum(coal_added[k] for k in range(max(0, t - data['CoalLife'] + 1), t + 1))
    nuke_lifetime_sum = pulp.lpSum(nuke_added[k] for k in range(max(0, t - data['NukeLife'] + 1), t + 1))
    
    # Demand satisfaction
    problem += data['OilCap'][t] + coal_lifetime_sum + nuke_lifetime_sum >= data['Demand'][t]
    
    # Nuclear proportion constraint
    total_capacity = data['OilCap'][t] + coal_lifetime_sum + nuke_lifetime_sum
    problem += nuke_lifetime_sum <= data['MaxNuke'] / 100 * total_capacity

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')