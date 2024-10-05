from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value, LpInteger

# Problem data
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

# Extract data
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100.0
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create a LP problem
problem = LpProblem("Electricity_Capacity_Planning", LpMinimize)

# Decision variables
coal_add = LpVariable.dicts("CoalAdd", (range(T),), lowBound=0, cat=LpInteger)
nuke_add = LpVariable.dicts("NukeAdd", (range(T),), lowBound=0, cat=LpInteger)

# Objective function
problem += lpSum(coal_cost * coal_add[t] + nuke_cost * nuke_add[t] for t in range(T))

# Constraints
for t in range(T):
    coal_cap = lpSum(coal_add[max(0, t - k)] for k in range(min(t + 1, coal_life)))
    nuke_cap = lpSum(nuke_add[max(0, t - k)] for k in range(min(t + 1, nuke_life)))
    
    # Total capacity must meet demand
    problem += (coal_cap + nuke_cap + oil_cap[t] >= demand[t])
    
    # Nuclear capacity constraint
    problem += (nuke_cap <= max_nuke * (coal_cap + nuke_cap + oil_cap[t]))

# Solve the problem
problem.solve()

# Prepare output
coal_cap_added = [value(coal_add[t]) for t in range(T)]
nuke_cap_added = [value(nuke_add[t]) for t in range(T)]
total_cost = value(problem.objective)

output = {
    "coal_cap_added": coal_cap_added,
    "nuke_cap_added": nuke_cap_added,
    "total_cost": total_cost,
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')