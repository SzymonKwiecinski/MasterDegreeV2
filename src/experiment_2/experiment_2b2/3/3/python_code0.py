import pulp

# Extract data from JSON
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

# Initialize the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Time periods
T = data['T']

# Parameters
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100.0
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Decision variables: Coal and Nuclear capacity added in each year
coal_cap_added = pulp.LpVariable.dicts("CoalCap", range(T), lowBound=0, cat='Continuous')
nuke_cap_added = pulp.LpVariable.dicts("NukeCap", range(T), lowBound=0, cat='Continuous')

# Objective function: Minimize cost
problem += pulp.lpSum([coal_cap_added[t] * coal_cost + nuke_cap_added[t] * nuke_cost for t in range(T)])

# Constraints

# Demand satisfaction constraint in each year
for t in range(T):
    coal_cap_active = pulp.lpSum([coal_cap_added[j] for j in range(max(0, t-coal_life+1), t+1)])
    nuke_cap_active = pulp.lpSum([nuke_cap_added[j] for j in range(max(0, t-nuke_life+1), t+1)])
    
    problem += (oil_cap[t] + coal_cap_active + nuke_cap_active >= demand[t], f"Demand_Constraint_Year_{t}")

# Nuclear capacity constraint in each year
for t in range(T):
    coal_cap_active = pulp.lpSum([coal_cap_added[j] for j in range(max(0, t-coal_life+1), t+1)])
    nuke_cap_active = pulp.lpSum([nuke_cap_added[j] for j in range(max(0, t-nuke_life+1), t+1)])
    
    total_cap = oil_cap[t] + coal_cap_active + nuke_cap_active
    problem += (nuke_cap_active <= max_nuke * total_cap, f"Nuclear_Capacity_Constraint_Year_{t}")

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "coal_cap_added": [pulp.value(coal_cap_added[t]) for t in range(T)],
    "nuke_cap_added": [pulp.value(nuke_cap_added[t]) for t in range(T)],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')