import pulp

# Parsing data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 
        'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke_percent = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Initialize the problem
problem = pulp.LpProblem("Electric_Capacity_Planning", pulp.LpMinimize)

# Decision variables
coal_cap_added = pulp.LpVariable.dicts("Coal_Cap_Added", range(T), lowBound=0, cat='Continuous')
nuke_cap_added = pulp.LpVariable.dicts("Nuke_Cap_Added", range(T), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum([coal_cost * coal_cap_added[t] + nuke_cost * nuke_cap_added[t] for t in range(T)])

# Constraints
for t in range(T):
    # Ensure that the total capacity each year meets the demand
    coal_contribution = pulp.lpSum([coal_cap_added[j] for j in range(max(0, t - coal_life + 1), t+1)])
    nuke_contribution = pulp.lpSum([nuke_cap_added[j] for j in range(max(0, t - nuke_life + 1), t+1)])
    
    problem += (oil_cap[t] + coal_contribution + nuke_contribution >= demand[t], f"Demand_Constraint_Year_{t}")

    # Ensure that no more than max_nuke_percent of the total capacity is nuclear
    total_cap = oil_cap[t] + coal_contribution + nuke_contribution
    problem += (nuke_contribution <= max_nuke_percent / 100.0 * total_cap, f"Nuke_Percentage_Constraint_Year_{t}")

# Solve problem
problem.solve(pulp.PULP_CBC_CMD(msg=False))

# Collect results
coal_cap_plan = [coal_cap_added[t].varValue for t in range(T)]
nuke_cap_plan = [nuke_cap_added[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

# Output
output = {
    "coal_cap_added": coal_cap_plan,
    "nuke_cap_added": nuke_cap_plan,
    "total_cost": total_cost,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')