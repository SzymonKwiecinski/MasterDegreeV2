import pulp

# Data
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
max_nuke = data['MaxNuke'] / 100
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Problem
problem = pulp.LpProblem("Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal_vars = pulp.LpVariable.dicts("coal", (t for t in range(T)), lowBound=0, cat=pulp.LpContinuous)
nuke_vars = pulp.LpVariable.dicts("nuke", (t for t in range(T)), lowBound=0, cat=pulp.LpContinuous)

# Objective Function
problem += pulp.lpSum(coal_cost * coal_vars[t] + nuke_cost * nuke_vars[t] for t in range(T)), "Total Cost"

# Constraints

# Capacity Constraint
for t in range(T):
    coal_sum = pulp.lpSum(coal_vars[t - j] for j in range(min(t, coal_life)))
    nuke_sum = pulp.lpSum(nuke_vars[t - k] for k in range(min(t, nuke_life)))
    problem += oil_cap[t] + coal_sum + nuke_sum >= demand[t], f"DemandConstraint_{t}"

# Nuclear Capacity Limit
for t in range(T):
    nuke_sum = pulp.lpSum(nuke_vars[t - k] for k in range(min(t, nuke_life)))
    coal_sum = pulp.lpSum(coal_vars[t - j] for j in range(min(t, coal_life)))
    problem += nuke_sum <= max_nuke * (oil_cap[t] + coal_sum + nuke_sum), f"NukeLimit_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')