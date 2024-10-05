import pulp

# Data given in JSON format
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke_percentage = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Creating a LP Minimization problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Define decision variables
coal_cap = pulp.LpVariable.dicts("CoalCapacityAdded", range(T), lowBound=0, cat='Continuous')
nuke_cap = pulp.LpVariable.dicts("NukeCapacityAdded", range(T), lowBound=0, cat='Continuous')

# Objective function: Minimize total cost
total_cost = pulp.lpSum([coal_cost * coal_cap[t] for t in range(T)]) + pulp.lpSum([nuke_cost * nuke_cap[t] for t in range(T)])
problem += total_cost

# Capacity constraints
for t in range(T):
    # Total capacity available in year t
    coal_available = pulp.lpSum([coal_cap[i] for i in range(max(0, t - coal_life + 1), t + 1)])
    nuke_available = pulp.lpSum([nuke_cap[j] for j in range(max(0, t - nuke_life + 1), t + 1)])
    total_capacity = oil_cap[t] + coal_available + nuke_available
    
    # Demand satisfaction constraint
    problem += (total_capacity >= demand[t], f"Demand_Constraint_Year_{t}")

    # Nuclear capacity percentage constraint
    if total_capacity > 0:
        problem += (nuke_available <= max_nuke_percentage / 100.0 * total_capacity, f"Nuke_Constraint_Year_{t}")

# Solve the problem
problem.solve()

# Extracting results
coal_cap_added = [pulp.value(coal_cap[t]) for t in range(T)]
nuke_cap_added = [pulp.value(nuke_cap[t]) for t in range(T)]
total_cost_value = pulp.value(total_cost)

# Output format
output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')