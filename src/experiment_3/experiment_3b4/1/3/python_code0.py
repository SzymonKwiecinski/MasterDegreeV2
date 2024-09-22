import pulp

# Data from the JSON
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
max_nuke = data['MaxNuke']
coal_life = data['CoalLife']
nuke_life = data['NukeLife']

# Create the Linear Programming problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

# Decision variables
x_coal = {t: pulp.LpVariable(f"x_coal_{t}", lowBound=0, cat='Continuous') for t in range(1, T+1)}
x_nuke = {t: pulp.LpVariable(f"x_nuke_{t}", lowBound=0, cat='Continuous') for t in range(1, T+1)}

# Objective function
problem += pulp.lpSum(coal_cost * x_coal[t] + nuke_cost * x_nuke[t] for t in range(1, T+1))

# Constraints
for t in range(1, T+1):
    coal_cap_t = pulp.lpSum(x_coal[j] for j in range(max(1, t-coal_life+1), t+1))
    nuke_cap_t = pulp.lpSum(x_nuke[k] for k in range(max(1, t-nuke_life+1), t+1))
    
    # Demand satisfaction
    problem += oil_cap[t-1] + coal_cap_t + nuke_cap_t >= demand[t-1]
    
    # Nuclear capacity limit
    problem += nuke_cap_t <= max_nuke * (oil_cap[t-1] + coal_cap_t + nuke_cap_t) / 100

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')