import pulp

# Data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}

# Parameters
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100.0
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision Variables
coal_cap_added = pulp.LpVariable.dicts("CoalCapAdded", range(T), lowBound=0, cat='Continuous')
nuke_cap_added = pulp.LpVariable.dicts("NukeCapAdded", range(T), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([coal_cost * coal_cap_added[t] + nuke_cost * nuke_cap_added[t] for t in range(T)])

# Constraints
for t in range(T):
    total_coal = sum(coal_cap_added[i] for i in range(max(0, t - coal_life + 1), t + 1))
    total_nuke = sum(nuke_cap_added[i] for i in range(max(0, t - nuke_life + 1), t + 1))
    
    # Capacity constraints
    problem += (oil_cap[t] + total_coal + total_nuke >= demand[t], f"Demand_Year_{t}")
    
    # Nuclear capacity percentage
    problem += (total_nuke <= max_nuke * (oil_cap[t] + total_coal + total_nuke), f"MaxNuke_Year_{t}")

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "coal_cap_added": [coal_cap_added[t].varValue for t in range(T)],
    "nuke_cap_added": [nuke_cap_added[t].varValue for t in range(T)],
    "total_cost": pulp.value(problem.objective)
}

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the result
output