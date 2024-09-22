import pulp

# Data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100.0
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create a LP minimization problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Variables
coal_cap_added = pulp.LpVariable.dicts("CoalCapAdded", range(T), lowBound=0)
nuke_cap_added = pulp.LpVariable.dicts("NukeCapAdded", range(T), lowBound=0)

# Objective
problem += pulp.lpSum(coal_cost * coal_cap_added[t] + nuke_cost * nuke_cap_added[t] for t in range(T))

# Constraints
for t in range(T):
    # Calculate available coal and nuclear capacity for year t
    available_coal_cap = sum(coal_cap_added[j] for j in range(max(0, t - coal_life + 1), t + 1))
    available_nuke_cap = sum(nuke_cap_added[j] for j in range(max(0, t - nuke_life + 1), t + 1))
    
    # Total capacity must meet demand
    problem += oil_cap[t] + available_coal_cap + available_nuke_cap >= demand[t]
    
    # Percentage of nuclear capacity constraint
    problem += available_nuke_cap <= max_nuke * (oil_cap[t] + available_coal_cap + available_nuke_cap)

# Solve the problem
problem.solve()

# Retrieve the results
coal_cap_plan = [coal_cap_added[t].varValue for t in range(T)]
nuke_cap_plan = [nuke_cap_added[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

# Output result
output = {
    "coal_cap_added": coal_cap_plan,
    "nuke_cap_added": nuke_cap_plan,
    "total_cost": total_cost,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')