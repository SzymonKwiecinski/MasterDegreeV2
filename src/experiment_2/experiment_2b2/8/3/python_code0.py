import pulp

# Data input as provided
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

# Extract the data
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100.0  # converting percentage
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Initialize the LP problem
problem = pulp.LpProblem("ElectricityCapacityPlanning", pulp.LpMinimize)

# Decision variables
coal_cap_added = [pulp.LpVariable(f'CoalAdded_{t}', lowBound=0) for t in range(T)]
nuke_cap_added = [pulp.LpVariable(f'NukeAdded_{t}', lowBound=0) for t in range(T)]

# Objective function: Minimize total capital cost
total_cost = pulp.lpSum([
    coal_cost * coal_cap_added[t] + nuke_cost * nuke_cap_added[t]
    for t in range(T)
])
problem += total_cost

# Constraints

# Ensure demand is met each year
for t in range(T):
    # Calculate available capacities by summing the capacities added over the respective lifespans
    coal_capacity = pulp.lpSum(coal_cap_added[max(0, t-l):t+1] for l in range(coal_life)) if t >= coal_life else pulp.lpSum(coal_cap_added[:t+1])
    nuke_capacity = pulp.lpSum(nuke_cap_added[max(0, t-l):t+1] for l in range(nuke_life)) if t >= nuke_life else pulp.lpSum(nuke_cap_added[:t+1])
    total_capacity = oil_cap[t] + coal_capacity + nuke_capacity
    problem += total_capacity >= demand[t], f'Demand_Constraint_{t}'

# Nuclear capacity constraints
for t in range(T):
    # Calculate available nuclear capacity similarly to coal
    nuke_capacity = pulp.lpSum(nuke_cap_added[max(0, t-l):t+1] for l in range(nuke_life)) if t >= nuke_life else pulp.lpSum(nuke_cap_added[:t+1])
    problem += nuke_capacity <= max_nuke * (oil_cap[t] + nuke_capacity + pulp.lpSum(coal_cap_added[max(0, t-l):t+1] for l in range(coal_life)) if t >= coal_life else pulp.lpSum(coal_cap_added[:t+1])), f'Nuke_Capacity_Constraint_{t}'

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "coal_cap_added": [pulp.value(coal_cap_added[t]) for t in range(T)],
    "nuke_cap_added": [pulp.value(nuke_cap_added[t]) for t in range(T)],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f'Objective Value: <OBJ>{pulp.value(problem.objective)}</OBJ>')