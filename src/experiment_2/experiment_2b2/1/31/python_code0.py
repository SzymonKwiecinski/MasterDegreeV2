import pulp

# Given data
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Extracting data from the json
demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

T = len(demand)  # Number of time periods
K = len(num)     # Number of generator types

# Problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
numon = [[pulp.LpVariable(f"numon_{k}_{t}", 0, num[k], cat='Integer') for t in range(T)] for k in range(K)]
output_above_min = [[pulp.LpVariable(f"output_above_min_{k}_{t}", 0, maxlevel[k] - minlevel[k]) for t in range(T)] for k in range(K)]

# Objective function
problem += pulp.lpSum([
    numon[k][t] * (runcost[k] + startcost[k]) +
    output_above_min[k][t] * extracost[k]
    for k in range(K) for t in range(T)
])

# Constraints
for t in range(T):
    # Ensure demand is met
    problem += pulp.lpSum([numon[k][t] * minlevel[k] + output_above_min[k][t] for k in range(K)]) >= demand[t]
    
    for k in range(K):
        # Output above min level should be valid
        problem += output_above_min[k][t] <= (maxlevel[k] - minlevel[k]) * numon[k][t]

# Solve the problem
problem.solve()

# Retrieve solution
numon_solution = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]

# Formulate the output
output = {
    "numon": numon_solution
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')