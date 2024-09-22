import pulp
import json

# Given data in JSON format
data = json.loads("{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}")

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Define decision variables
coal_capacity = pulp.LpVariable.dicts("Coal", range(1, T+1), lowBound=0)
nuke_capacity = pulp.LpVariable.dicts("Nuke", range(1, T+1), lowBound=0)

# Objective function
problem += pulp.lpSum(coal_cost * coal_capacity[t] + nuke_cost * nuke_capacity[t] for t in range(1, T+1))

# Demand constraints
for t in range(1, T+1):
    problem += (oil_cap[t-1] + pulp.lpSum(coal_capacity[s] for s in range(1, t+1)) +
                 pulp.lpSum(nuke_capacity[s] for s in range(1, t+1)) >= demand[t-1])

# Nuclear capacity constraint
for t in range(1, T+1):
    problem += (pulp.lpSum(nuke_capacity[s] for s in range(1, t+1)) <= 
                 (max_nuke / 100) * (oil_cap[t-1] + pulp.lpSum(coal_capacity[s] for s in range(1, t+1)) +
                 pulp.lpSum(nuke_capacity[s] for s in range(1, t+1))))

# Lifetime constraints
for t in range(1, T+1):
    for s in range(1, t - coal_life + 1):
        problem += coal_capacity[s] == 0
    for s in range(1, t - nuke_life + 1):
        problem += nuke_capacity[s] == 0

# Solve the problem
problem.solve()

# Output results
coal_cap_added = [coal_capacity[t].varValue for t in range(1, T+1)]
nuke_cap_added = [nuke_capacity[t].varValue for t in range(1, T+1)]
total_cost = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
print("Coal Capacity Added:", coal_cap_added)
print("Nuclear Capacity Added:", nuke_cap_added)