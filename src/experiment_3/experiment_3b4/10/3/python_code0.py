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

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision Variables
coal_added = pulp.LpVariable.dicts("coal_added", range(T), lowBound=0, cat='Continuous')
nuke_added = pulp.LpVariable.dicts("nuke_added", range(T), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([coal_cost * coal_added[t] + nuke_cost * nuke_added[t] for t in range(T)])

# Constraints

# 1. Demand Satisfaction
for t in range(T):
    coal_capacity = pulp.lpSum([coal_added[max(0, t - k)] for k in range(min(t, coal_life))])
    nuke_capacity = pulp.lpSum([nuke_added[max(0, t - k)] for k in range(min(t, nuke_life))])
    problem += oil_cap[t] + coal_capacity + nuke_capacity >= demand[t]

# 2. Nuclear Capacity Limit
for t in range(T):
    nuke_capacity = pulp.lpSum([nuke_added[max(0, t - k)] for k in range(min(t, nuke_life))])
    total_capacity = oil_cap[t] + coal_capacity + nuke_capacity
    problem += nuke_capacity <= (max_nuke / 100) * total_capacity

# Solve the problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')