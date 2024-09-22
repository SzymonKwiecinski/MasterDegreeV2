import pulp

# Problem Initialization
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

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

# Decision Variables
coal_add = pulp.LpVariable.dicts("CoalAdded", range(T), lowBound=0, cat='Continuous')
nuke_add = pulp.LpVariable.dicts("NukeAdded", range(T), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([coal_cost * coal_add[t] + nuke_cost * nuke_add[t] for t in range(T)])

# Constraints

# Demand Satisfaction Constraints
for t in range(T):
    coal_active_cap = pulp.lpSum(coal_add[i] for i in range(max(0, t+1-coal_life), t+1))
    nuke_active_cap = pulp.lpSum(nuke_add[j] for j in range(max(0, t+1-nuke_life), t+1))
    problem += oil_cap[t] + coal_active_cap + nuke_active_cap >= demand[t]

# Total Capacity Constraint
for t in range(T):
    total_coal_cap = pulp.lpSum(coal_add[i] for i in range(T))
    total_nuke_cap = pulp.lpSum(nuke_add[j] for j in range(T))
    problem += pulp.lpSum(nuke_add[j] for j in range(t+1)) <= (max_nuke / 100) * (oil_cap[t] + total_coal_cap + total_nuke_cap)

# Solve the problem
problem.solve()

# Output
coal_cap_added = [pulp.value(coal_add[t]) for t in range(T)]
nuke_cap_added = [pulp.value(nuke_add[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')