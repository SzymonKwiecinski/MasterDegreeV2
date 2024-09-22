import pulp

# Data from JSON format
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

# Create the Linear Programming problem
problem = pulp.LpProblem("Capacity_Expansion_Planning", pulp.LpMinimize)

# Decision Variables
c = [pulp.LpVariable(f'coal_{t}', lowBound=0, cat='Continuous') for t in range(1, data['T'] + 1)]
n = [pulp.LpVariable(f'nuke_{t}', lowBound=0, cat='Continuous') for t in range(1, data['T'] + 1)]

# Objective Function
problem += pulp.lpSum(data['CoalCost'] * c[t] + data['NukeCost'] * n[t] for t in range(data['T'])), "Total_Cost"

# Constraints
for t in range(data['T']):
    # Demand satisfaction constraint for each year t
    coal_terms = [c[j] for j in range(max(0, t - data['CoalLife'] + 1), t + 1)]
    nuke_terms = [n[j] for j in range(max(0, t - data['NukeLife'] + 1), t + 1)]
    total_capacity = data['OilCap'][t] + pulp.lpSum(coal_terms) + pulp.lpSum(nuke_terms)
    problem += total_capacity >= data['Demand'][t], f"Demand_Satisfaction_{t+1}"

    # Nuclear capacity limitation constraint
    problem += pulp.lpSum(nuke_terms) <= data['MaxNuke'] / 100 * total_capacity, f"Nuke_Limit_{t+1}"

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')