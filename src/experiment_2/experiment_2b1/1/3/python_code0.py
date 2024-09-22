import pulp
import json

# Input data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
        'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100.0
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Problem Definition
problem = pulp.LpProblem("ElectricityCapacityExpansion", pulp.LpMinimize)

# Decision variables
coal_cap = pulp.LpVariable.dicts("CoalCap", range(T), lowBound=0, cat='Continuous')
nuke_cap = pulp.LpVariable.dicts("NukeCap", range(T), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(coal_cost * coal_cap[t] for t in range(T)) + pulp.lpSum(nuke_cost * nuke_cap[t] for t in range(T)), "Total Cost"

# Constraints
for t in range(T):
    total_capacity = oil_cap[t] + pulp.lpSum(coal_cap[j] for j in range(max(0, t - coal_life + 1), t + 1)) + \
                             pulp.lpSum(nuke_cap[j] for j in range(max(0, t - nuke_life + 1), t + 1))

    problem += total_capacity >= demand[t], f"Demand_Constraint_{t}"

# Nuclear capacity constraint
for t in range(T):
    total_capacity = oil_cap[t] + pulp.lpSum(coal_cap[j] for j in range(max(0, t - coal_life + 1), t + 1)) + \
                             pulp.lpSum(nuke_cap[j] for j in range(max(0, t - nuke_life + 1), t + 1))

    nuclear_capacity = pulp.lpSum(nuke_cap[j] for j in range(max(0, t - nuke_life + 1), t + 1))

    problem += nuclear_capacity <= max_nuke * total_capacity, f"Nuke_Capacity_Constraint_{t}"

# Solve the problem
problem.solve()

# Collect the results
coal_cap_added = [coal_cap[t].varValue for t in range(T)]
nuke_cap_added = [nuke_cap[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

# Format output
output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')