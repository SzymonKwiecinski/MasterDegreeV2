import pulp

# Data from JSON
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Define the LP problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision variables
coal_cap_added = pulp.LpVariable.dicts("CoalCapAdded", range(T), lowBound=0, cat='Continuous')
nuke_cap_added = pulp.LpVariable.dicts("NukeCapAdded", range(T), lowBound=0, cat='Continuous')

# Objective: Minimize total cost
total_cost = pulp.lpSum([coal_cost * coal_cap_added[t] + nuke_cost * nuke_cap_added[t] for t in range(T)])
problem += total_cost

# Constraints
for t in range(T):
    # Capacity constraint
    coal_capacity = pulp.lpSum([coal_cap_added[j] for j in range(max(0, t-coal_life+1), t+1)])
    nuke_capacity = pulp.lpSum([nuke_cap_added[j] for j in range(max(0, t-nuke_life+1), t+1)])
    
    problem += (oil_cap[t] + coal_capacity + nuke_capacity >= demand[t])
    
    # Nuclear percentage constraint
    problem += (nuke_capacity <= max_nuke * (oil_cap[t] + coal_capacity + nuke_capacity))

# Solve the problem
problem.solve()

# Collect the results
coal_cap_added_solution = [coal_cap_added[t].varValue for t in range(T)]
nuke_cap_added_solution = [nuke_cap_added[t].varValue for t in range(T)]
total_cost_solution = pulp.value(problem.objective)

# Output format
output = {
    "coal_cap_added": coal_cap_added_solution,
    "nuke_cap_added": nuke_cap_added_solution,
    "total_cost": total_cost_solution,
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost_solution}</OBJ>')