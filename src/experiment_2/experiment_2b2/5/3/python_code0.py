import pulp

# Data from JSON input
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
max_nuke_percentage = data['MaxNuke'] / 100.0
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create a LP problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Variables
coal_cap_added = pulp.LpVariable.dicts("CoalCapAdded", range(T), 0, None, cat='Continuous')
nuke_cap_added = pulp.LpVariable.dicts("NukeCapAdded", range(T), 0, None, cat='Continuous')

# Objective: Minimize total investment cost
problem += pulp.lpSum([coal_cost * coal_cap_added[t] + nuke_cost * nuke_cap_added[t] for t in range(T)]), "TotalCost"

# Constraints
for t in range(T):
    # Demand satisfaction
    total_coal = pulp.lpSum([coal_cap_added[j] for j in range(max(0, t-coal_life+1), t+1)])
    total_nuke = pulp.lpSum([nuke_cap_added[j] for j in range(max(0, t-nuke_life+1), t+1)])
    problem += (oil_cap[t] + total_coal + total_nuke >= demand[t]), f"DemandConstraint_{t}"
    
    # Nuclear capacity percentage constraint
    problem += (total_nuke <= max_nuke_percentage * (oil_cap[t] + total_coal + total_nuke)), f"MaxNukeConstraint_{t}"

# Solve the problem
problem.solve()

# Output preparation
output = {
    "coal_cap_added": [coal_cap_added[t].varValue for t in range(T)],
    "nuke_cap_added": [nuke_cap_added[t].varValue for t in range(T)],
    "total_cost": pulp.value(problem.objective)
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
output