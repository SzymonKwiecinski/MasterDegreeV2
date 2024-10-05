import pulp

# Data from JSON
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

# Parameters
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision Variables
coal_cap_added = {t: pulp.LpVariable(f'coal_cap_added_{t}', lowBound=0) for t in range(1, T+1)}
nuke_cap_added = {t: pulp.LpVariable(f'nuke_cap_added_{t}', lowBound=0) for t in range(1, T+1)}

# Objective Function
total_cost = pulp.lpSum(coal_cost * coal_cap_added[t] + nuke_cost * nuke_cap_added[t] for t in range(1, T+1))
problem += total_cost

# Constraints

# Demand Satisfaction
for t in range(1, T+1):
    coal_capacity = pulp.lpSum(coal_cap_added[k] for k in range(max(1, t-coal_life+1), t+1))
    nuke_capacity = pulp.lpSum(nuke_cap_added[k] for k in range(max(1, t-nuke_life+1), t+1))
    
    problem += coal_capacity + nuke_capacity + oil_cap[t-1] >= demand[t-1], f"Demand_Constraint_{t}"

# Nuclear Capacity Limit
for t in range(1, T+1):
    nuke_capacity = pulp.lpSum(nuke_cap_added[k] for k in range(max(1, t-nuke_life+1), t+1))
    total_capacity = pulp.lpSum(coal_cap_added[k] for k in range(max(1, t-coal_life+1), t+1)) + nuke_capacity + oil_cap[t-1]
    
    problem += nuke_capacity <= max_nuke / 100.0 * total_capacity, f"Nuke_Capacity_Limit_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')