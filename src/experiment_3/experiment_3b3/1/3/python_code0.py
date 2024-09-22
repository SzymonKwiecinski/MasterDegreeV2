import pulp

# Data provided
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

# Define the problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Parameters
T = data['T']
Demand = data['Demand']
OilCap = data['OilCap']
CoalCost = data['CoalCost']
NukeCost = data['NukeCost']
MaxNuke = data['MaxNuke']
CoalLife = data['CoalLife']
NukeLife = data['NukeLife']

# Decision variables
coal_vars = [pulp.LpVariable(f'coal_{t}', lowBound=0, cat='Continuous') for t in range(T)]
nuke_vars = [pulp.LpVariable(f'nuke_{t}', lowBound=0, cat='Continuous') for t in range(T)]

# Objective function
problem += pulp.lpSum(CoalCost * coal_vars[t] + NukeCost * nuke_vars[t] for t in range(T)), "Total_Cost"

# Constraints

# Demand Constraint
for t in range(T):
    coal_lifetime_range = range(max(0, t - CoalLife + 1), t + 1)
    nuke_lifetime_range = range(max(0, t - NukeLife + 1), t + 1)
    
    problem += (OilCap[t] 
                + pulp.lpSum(coal_vars[j] for j in coal_lifetime_range) 
                + pulp.lpSum(nuke_vars[j] for j in nuke_lifetime_range) 
                >= Demand[t]), f'Demand_Constraint_{t}'

# Nuclear Capacity Constraint
for t in range(T):
    problem += (pulp.lpSum(nuke_vars[j] for j in range(t + 1))
                <= (MaxNuke / 100) * (OilCap[t] 
                                      + pulp.lpSum(coal_vars[j] for j in range(t + 1)) 
                                      + pulp.lpSum(nuke_vars[j] for j in range(t + 1)))), f'Nuke_Capacity_Constraint_{t}'

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "coal_cap_added": [pulp.value(coal_vars[t]) for t in range(T)],
    "nuke_cap_added": [pulp.value(nuke_vars[t]) for t in range(T)],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')