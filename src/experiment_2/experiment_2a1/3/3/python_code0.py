import pulp
import json

# Input data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
        'CoalCost': 10, 
        'NukeCost': 5, 
        'MaxNuke': 20, 
        'CoalLife': 5, 
        'NukeLife': 10}

T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100.0
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Define variables
coal_cap_added = pulp.LpVariable.dicts("CoalAdded", range(T), lowBound=0, cat='Continuous')
nuke_cap_added = pulp.LpVariable.dicts("NukeAdded", range(T), lowBound=0, cat='Continuous')

# Objective function
problem += (pulp.lpSum(coal_cap_added[t] * coal_cost for t in range(T)) + 
             pulp.lpSum(nuke_cap_added[t] * nuke_cost for t in range(T))), "Total Cost"

# Constraints
for t in range(T):
    total_capacity = oil_cap[t] + pulp.lpSum(coal_cap_added[year] for year in range(max(0, t-coal_life+1), t+1)) + \
                                               pulp.lpSum(nuke_cap_added[year] for year in range(max(0, t-nuke_life+1), t+1))
    # Demand must be met
    problem += total_capacity >= demand[t], f"Demand_Constraint_{t}"
    
for t in range(T):
    # Nuclear capacity should not exceed max_nuke% of total capacity
    problem += pulp.lpSum(nuke_cap_added[year] for year in range(max(0, t-nuke_life+1), t+1)) <= max_nuke * total_capacity, f"Nuke_Capacity_Constraint_{t}"

# Solve the problem
problem.solve()

# Prepare the output
coal_added = [coal_cap_added[t].varValue for t in range(T)]
nuke_added = [nuke_cap_added[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_added,
    "nuke_cap_added": nuke_added,
    "total_cost": total_cost
}

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')