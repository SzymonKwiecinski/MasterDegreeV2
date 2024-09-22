import pulp
import json

# Given data in JSON format
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

# Extract parameters
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke_percentage = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal = pulp.LpVariable.dicts("coal", range(1, T + 1), lowBound=0)
nuke = pulp.LpVariable.dicts("nuke", range(1, T + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum([coal_cost * coal[t] + nuke_cost * nuke[t] for t in range(1, T + 1)])

# Constraints
# Demand constraints
for t in range(1, T + 1):
    coal_sum = pulp.lpSum([coal[s] for s in range(max(1, t - coal_life + 1), t + 1)])
    nuke_sum = pulp.lpSum([nuke[s] for s in range(max(1, t - nuke_life + 1), t + 1)])
    problem += (coal_sum + nuke_sum + oil_capacity[t - 1] >= demand[t - 1])

# Nuclear capacity limit constraints
for t in range(1, T + 1):
    left_side = pulp.lpSum([nuke[s] for s in range(1, t + 1)])
    right_side = (max_nuke_percentage / 100) * (
        pulp.lpSum([coal[s] for s in range(1, t + 1)]) + 
        pulp.lpSum([nuke[s] for s in range(1, t + 1)]) + 
        pulp.lpSum([oil_capacity[s - 1] for s in range(1, t + 1)])
    )
    problem += (left_side <= right_side)

# Solve the problem
problem.solve()

# Extracting results
coal_cap_added = [coal[t].varValue for t in range(1, T + 1)]
nuke_cap_added = [nuke[t].varValue for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

# Output results
print(f'Coal capacity added each year: {coal_cap_added}')
print(f'Nuclear capacity added each year: {nuke_cap_added}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')