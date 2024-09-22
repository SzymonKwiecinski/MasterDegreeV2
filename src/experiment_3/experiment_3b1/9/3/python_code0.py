import pulp
import json

# Input Data
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

# Model Initialization
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision Variables
coal = pulp.LpVariable.dicts("Coal", range(1, data['T'] + 1), lowBound=0, cat='Continuous')
nuke = pulp.LpVariable.dicts("Nuke", range(1, data['T'] + 1), lowBound=0, cat='Continuous')

# Objective Function
total_cost = pulp.lpSum(data['CoalCost'] * coal[t] + data['NukeCost'] * nuke[t] for t in range(1, data['T'] + 1))
problem += total_cost

# Constraints
# 1. Capacity requirement
for t in range(1, data['T'] + 1):
    coal_capacity = pulp.lpSum(coal[j] for j in range(max(1, t - data['CoalLife'] + 1), t + 1))
    nuke_capacity = pulp.lpSum(nuke[j] for j in range(max(1, t - data['NukeLife'] + 1), t + 1))
    problem += (coal_capacity + nuke_capacity + data['OilCap'][t - 1] >= data['Demand'][t - 1])

# 2. Nuclear capacity limit
for t in range(1, data['T'] + 1):
    problem += (pulp.lpSum(nuke[j] for j in range(1, t + 1)) /
                (pulp.lpSum(coal[j] + nuke[j] for j in range(1, t + 1)) + 
                 pulp.lpSum(data['OilCap'][j - 1] for j in range(1, t + 1))) <= 
                data['MaxNuke'] / 100)

# Solve the problem
problem.solve()

# Collecting results
coal_cap_added = [coal[t].varValue for t in range(1, data['T'] + 1)]
nuke_cap_added = [nuke[t].varValue for t in range(1, data['T'] + 1)]
total_cost_value = pulp.value(problem.objective)

# Output
output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')