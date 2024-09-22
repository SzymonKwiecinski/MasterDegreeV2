import pulp
import json

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

# Decision Variables
coal_vars = pulp.LpVariable.dicts("coal", range(1, T + 1), lowBound=0, cat='Continuous')
nuke_vars = pulp.LpVariable.dicts("nuke", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(coal_cost * coal_vars[t] + nuke_cost * nuke_vars[t] for t in range(1, T + 1))

# Constraints
# Demand Satisfaction
for t in range(1, T + 1):
    demand_expr = (oil_cap[t - 1] + 
                   pulp.lpSum(coal_vars[max(1, t - i)] for i in range(1, min(t, coal_life) + 1)) +
                   pulp.lpSum(nuke_vars[max(1, t - j)] for j in range(1, min(t, nuke_life) + 1)))
    problem += (demand_expr >= demand[t - 1], f"Demand_Constraint_{t}")

# Maximum Nuclear Capacity
for j in range(1, T + 1):
    total_capacity = oil_cap[j - 1] + pulp.lpSum(coal_vars[max(1, j - i)] for i in range(1, min(j, coal_life) + 1)) + \
                    pulp.lpSum(nuke_vars[max(1, j - k)] for k in range(1, min(j, nuke_life) + 1))
    problem += (pulp.lpSum(nuke_vars[t] for t in range(1, T + 1)) / total_capacity <= max_nuke / 100, f"Nuclear_Capacity_Constraint_{j}")

# Solve the problem
problem.solve()

# Output results
coal_cap_added = [pulp.value(coal_vars[t]) for t in range(1, T + 1)]
nuke_cap_added = [pulp.value(nuke_vars[t]) for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')