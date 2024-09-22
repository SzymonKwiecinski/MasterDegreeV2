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

# Parameters
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the model
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal = pulp.LpVariable.dicts("coal", range(1, T + 1), lowBound=0)
nuke = pulp.LpVariable.dicts("nuke", range(1, T + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum([coal_cost * coal[t] + nuke_cost * nuke[t] for t in range(1, T + 1)])

# Constraints
for t in range(1, T + 1):
    problem += (pulp.lpSum([coal[s] for s in range(t, min(t + coal_life, T + 1))]) +
                 pulp.lpSum([nuke[s] for s in range(t, min(t + nuke_life, T + 1))]) +
                 oil_capacity[t - 1] >= demand[t - 1], f"Demand_Satisfaction_{t}")

for t in range(1, T + 1):
    problem += (pulp.lpSum([nuke[s] for s in range(1, t + 1)]) <=
                 (max_nuke / 100) * 
                 (oil_capacity[t - 1] +
                  pulp.lpSum([coal[s] for s in range(1, t + 1)]) +
                  pulp.lpSum([nuke[s] for s in range(1, t + 1)])), f"Nuclear_Capacity_Limitation_{t}")

# Solve the problem
problem.solve()

# Output results
coal_cap_added = [coal[t].varValue for t in range(1, T + 1)]
nuke_cap_added = [nuke[t].varValue for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

print(f'Coal Capacity Added: {coal_cap_added}')
print(f'Nuclear Capacity Added: {nuke_cap_added}')
print(f'Total Cost: <OBJ>{total_cost}</OBJ>')