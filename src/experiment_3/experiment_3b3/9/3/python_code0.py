import pulp

# Data from the provided JSON
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

# Initialize the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion_Planning", pulp.LpMinimize)

# Decision variables
coal_vars = pulp.LpVariable.dicts("coal", range(T), lowBound=0, cat='Continuous')
nuke_vars = pulp.LpVariable.dicts("nuke", range(T), lowBound=0, cat='Continuous')

# Objective function: Minimize total cost
problem += pulp.lpSum(coal_cost * coal_vars[t] + nuke_cost * nuke_vars[t] for t in range(T))

# Constraints

# Capacity Requirement Constraints
for t in range(T):
    coal_contrib = sum(coal_vars[j] for j in range(max(0, t - coal_life + 1), t + 1))
    nuke_contrib = sum(nuke_vars[j] for j in range(max(0, t - nuke_life + 1), t + 1))
    problem += oil_cap[t] + coal_contrib + nuke_contrib >= demand[t]

# Nuclear Capacity Limit Constraints
for t in range(T):
    total_capacity_t = oil_cap[t] + sum(coal_vars[j] for j in range(t + 1)) + sum(nuke_vars[j] for j in range(t + 1))
    problem += sum(nuke_vars[j] for j in range(t + 1)) <= (max_nuke / 100) * total_capacity_t

# Solve the problem
problem.solve()

# Retrieve results
coal_cap_added = [pulp.value(coal_vars[t]) for t in range(T)]
nuke_cap_added = [pulp.value(nuke_vars[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

# Output
print(f'Coal Capacity Added: {coal_cap_added}')
print(f'Nuke Capacity Added: {nuke_cap_added}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')