import pulp

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

# Unpack data
T = data['T']
Demand = data['Demand']
OilCap = data['OilCap']
CoalCost = data['CoalCost']
NukeCost = data['NukeCost']
MaxNuke = data['MaxNuke']
CoalLife = data['CoalLife']
NukeLife = data['NukeLife']

# Create the problem
problem = pulp.LpProblem("Capacity_Planning", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{t}', lowBound=0, cat='Continuous') for t in range(T)]
y = [pulp.LpVariable(f'y_{t}', lowBound=0, cat='Continuous') for t in range(T)]

# Objective function
problem += pulp.lpSum(CoalCost * x[t] + NukeCost * y[t] for t in range(T))

# Constraints
for t in range(T):
    # Demand Satisfaction
    coal_sum = pulp.lpSum(x[j] for j in range(max(0, t - CoalLife + 1), t + 1))
    nuke_sum = pulp.lpSum(y[j] for j in range(max(0, t - NukeLife + 1), t + 1))
    problem += (OilCap[t] + coal_sum + nuke_sum >= Demand[t])
    
    # Nuclear Capacity Limit
    if OilCap[t] + coal_sum + nuke_sum > 0:
        problem += (nuke_sum / (OilCap[t] + coal_sum + nuke_sum) <= MaxNuke / 100)

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')