import pulp
import json

# Data from the problem
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

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Variables
coal_capacity = pulp.LpVariable.dicts("CoalCapacity", range(1, data['T'] + 1), lowBound=0, cat='Continuous')
nuke_capacity = pulp.LpVariable.dicts("NuclearCapacity", range(1, data['T'] + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['CoalCost'] * coal_capacity[t] + data['NukeCost'] * nuke_capacity[t] for t in range(1, data['T'] + 1))

# Constraints
for t in range(1, data['T'] + 1):
    # Demand satisfaction constraint
    demand_satisfaction = pulp.lpSum(coal_capacity[t-j] for j in range(0, min(t, data['CoalLife']) + 1)) + \
                              pulp.lpSum(nuke_capacity[t-j] for j in range(0, min(t, data['NukeLife']) + 1)) + \
                              data['OilCap'][t - 1]
    problem += (demand_satisfaction >= data['Demand'][t - 1])

    # Capacity limitations constraint
    total_capacity = pulp.lpSum(coal_capacity[t-j] for j in range(0, min(t, data['CoalLife']) + 1)) + \
                     pulp.lpSum(nuke_capacity[t-j] for j in range(0, min(t, data['NukeLife']) + 1)) + \
                     data['OilCap'][t - 1]
    problem += (pulp.lpSum(coal_capacity[t-j] for j in range(0, min(t, data['CoalLife']) + 1)) + \
                  pulp.lpSum(nuke_capacity[t-j] for j in range(0, min(t, data['NukeLife']) + 1)) <= 
                  (data['MaxNuke'] / 100) * total_capacity)

# Solve the problem
problem.solve()

# Output results
coal_added = [coal_capacity[t].varValue for t in range(1, data['T'] + 1)]
nuke_added = [nuke_capacity[t].varValue for t in range(1, data['T'] + 1)]
total_cost = pulp.value(problem.objective)

# Prepare output
output = {
    "coal_cap_added": coal_added,
    "nuke_cap_added": nuke_added,
    "total_cost": total_cost
}

# Print the result
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')