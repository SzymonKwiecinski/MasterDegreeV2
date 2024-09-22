import pulp
import json

# Load data from the provided JSON format
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
        'CoalCost': 10, 
        'NukeCost': 5, 
        'MaxNuke': 20, 
        'CoalLife': 5, 
        'NukeLife': 10}

# Problem setup
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100  # Convert percentage to a fraction
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Planning", pulp.LpMinimize)

# Decision Variables
coal_cap = [pulp.LpVariable(f'CoalCap_{t}', lowBound=0, cat='Continuous') for t in range(T)]
nuke_cap = [pulp.LpVariable(f'NukeCap_{t}', lowBound=0, cat='Continuous') for t in range(T)]

# Objective Function
total_cost = pulp.lpSum([coal_cost * coal_cap[t] for t in range(T)]) + \
             pulp.lpSum([nuke_cost * nuke_cap[t] for t in range(T)])

problem += total_cost

# Constraints
for t in range(T):
    total_capacity = oil_cap[t] + pulp.lpSum([coal_cap[max(0, t - i)] for i in range(coal_life) if t - i >= 0]) + \
                         pulp.lpSum([nuke_cap[max(0, t - j)] for j in range(nuke_life) if t - j >= 0])
    
    # Demand must be met
    problem += total_capacity >= demand[t], f'Demand_Constraint_{t}'

    # Nuclear capacity constraint
    problem += pulp.lpSum([nuke_cap[t_] for t_ in range(T)]) <= max_nuke * total_capacity, f'Nuclear_Capacity_Constraint_{t}'

# Solve the problem
problem.solve()

# Prepare output
coal_cap_added = [coal_cap[t].varValue for t in range(T)]
nuke_cap_added = [nuke_cap[t].varValue for t in range(T)]
total_cost_value = pulp.value(problem.objective)

output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')