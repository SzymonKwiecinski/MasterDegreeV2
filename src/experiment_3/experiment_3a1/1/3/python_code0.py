import pulp

# Data from the provided JSON format
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

# Parameters
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision variables
coal = pulp.LpVariable.dicts("coal", range(1, T + 1), lowBound=0, cat='Continuous')
nuke = pulp.LpVariable.dicts("nuke", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(coal_cost * coal[t] + nuke_cost * nuke[t] for t in range(1, T + 1))

# Constraints

# Capacity Requirement
for t in range(1, T + 1):
    problem += (
        oil_capacity[t - 1] + 
        pulp.lpSum(coal[k] for k in range(max(1, t - coal_life + 1), t + 1)) + 
        pulp.lpSum(nuke[k] for k in range(max(1, t - nuke_life + 1), t + 1)) >= demand[t - 1],
        f"Capacity_Requirement_{t}"
    )

# Nuclear Capacity Limit
for t in range(1, T + 1):
    problem += (
        pulp.lpSum(nuke[k] for k in range(1, t + 1)) <= 
        (max_nuke / 100) * (oil_capacity[t - 1] + 
        pulp.lpSum(coal[k] for k in range(1, t + 1)) + 
        pulp.lpSum(nuke[k] for k in range(1, t + 1))),
        f"Nuclear_Capacity_Limit_{t}"
    )

# Solve the problem
problem.solve()

# Output results
coal_cap_added = [pulp.value(coal[t]) for t in range(1, T + 1)]
nuke_cap_added = [pulp.value(nuke[t]) for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

print(f'Coal capacity added each year: {coal_cap_added}')
print(f'Nuclear capacity added each year: {nuke_cap_added}')
print(f'Total cost of the capacity expansion: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')