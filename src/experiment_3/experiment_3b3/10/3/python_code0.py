import pulp

# Data
data = {
    'T': 12,
    'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35],
    'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5],
    'CoalCost': 10,
    'NukeCost': 5,
    'MaxNuke': 20,  # in percentage
    'CoalLife': 5,
    'NukeLife': 10
}

# Variables
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
coal_cost = data['CoalCost']
nuke_cost = data['NukeCost']
max_nuke = data['MaxNuke'] / 100  # convert percentage to proportion
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision Variables
coal_vars = pulp.LpVariable.dicts("Coal", range(T), lowBound=0, cat='Continuous')
nuke_vars = pulp.LpVariable.dicts("Nuke", range(T), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(coal_cost * coal_vars[t] + nuke_cost * nuke_vars[t] for t in range(T))

# Constraints

# Demand Constraints
for t in range(T):
    problem += (
        pulp.lpSum(coal_vars[i] for i in range(max(0, t - coal_life + 1), t + 1)) +
        pulp.lpSum(nuke_vars[j] for j in range(max(0, t - nuke_life + 1), t + 1)) +
        oil_cap[t] >= demand[t]
    )

# Nuclear Capacity Constraints
for t in range(T):
    total_capacity = pulp.lpSum(coal_vars[i] + nuke_vars[i] for i in range(t + 1)) + oil_cap[t]
    problem += (
        pulp.lpSum(nuke_vars[j] for j in range(t + 1)) <= max_nuke * total_capacity
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')