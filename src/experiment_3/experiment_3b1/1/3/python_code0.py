import pulp
import json

# Data input in JSON format
data = json.loads("{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}")

# Parameters
T = data['T']
demand = data['Demand']
oil_capacity = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the LP problem
problem = pulp.LpProblem("Electricity Capacity Expansion", pulp.LpMinimize)

# Decision Variables
x_c = pulp.LpVariable.dicts("Coal_Capacity_Added", range(1, T + 1), lowBound=0, cat='Continuous')
x_n = pulp.LpVariable.dicts("Nuclear_Capacity_Added", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(coal_cost * x_c[t] + nuke_cost * x_n[t] for t in range(1, T + 1)), "Total Cost"

# Constraints
for t in range(1, T + 1):
    problem += (oil_capacity[t - 1] + 
                 pulp.lpSum(x_c[j] for j in range(max(1, t - coal_life + 1), t + 1)) + 
                 pulp.lpSum(x_n[j] for j in range(max(1, t - nuke_life + 1), t + 1)) >= demand[t - 1], 
                 f"Capacity_Requirement_{t}")

for t in range(1, T + 1):
    problem += (pulp.lpSum(x_n[j] for j in range(1, t + 1)) <= 
                 (max_nuke / 100) * (oil_capacity[t - 1] + 
                                     pulp.lpSum(x_c[j] for j in range(1, t + 1)) + 
                                     pulp.lpSum(x_n[j] for j in range(1, t + 1))), 
                 f"Nuclear_Capacity_Limit_{t}")

# Solve the problem
problem.solve()

# Output results
coal_cap_added = [pulp.value(x_c[t]) for t in range(1, T + 1)]
nuke_cap_added = [pulp.value(x_n[t]) for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

print(f' coal_cap_added: {coal_cap_added}')
print(f' nuke_cap_added: {nuke_cap_added}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')