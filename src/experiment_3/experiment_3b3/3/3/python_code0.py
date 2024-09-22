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

# Problem Definition
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
C = [pulp.LpVariable(f'C_{t+1}', lowBound=0, cat='Continuous') for t in range(data['T'])]
N = [pulp.LpVariable(f'N_{t+1}', lowBound=0, cat='Continuous') for t in range(data['T'])]

# Objective Function
problem += pulp.lpSum([data['CoalCost'] * C[t] + data['NukeCost'] * N[t] for t in range(data['T'])])

# Constraints
for t in range(data['T']):
    coal_life_terms = [C[i] for i in range(max(0, t - data['CoalLife'] + 1), t + 1)]
    nuke_life_terms = [N[j] for j in range(max(0, t - data['NukeLife'] + 1), t + 1)]
    
    # 1. Capacity Constraint
    problem += (data['OilCap'][t] + pulp.lpSum(coal_life_terms) + pulp.lpSum(nuke_life_terms) >= data['Demand'][t])

    # 2. Nuclear Capacity Limit
    problem += (pulp.lpSum(nuke_life_terms) <= (data['MaxNuke'] / 100) * (data['OilCap'][t] + pulp.lpSum(coal_life_terms) + pulp.lpSum(nuke_life_terms)))

# Solve the problem
problem.solve()

# Output
coal_cap_added = [C[t].varValue for t in range(data['T'])]
nuke_cap_added = [N[t].varValue for t in range(data['T'])]
total_cost = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')