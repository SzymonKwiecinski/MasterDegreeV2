import pulp

# Load data from the JSON structure
data = {
    'demand': [15000, 30000, 25000, 40000, 27000], 
    'num': [12, 10, 5], 
    'minlevel': [850, 1250, 1500], 
    'maxlevel': [2000, 1750, 4000], 
    'runcost': [1000, 2600, 3000], 
    'extracost': [2.0, 1.3, 3.0], 
    'startcost': [2000, 1000, 500]
}

# Extract data
demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

T = len(demand)  # Number of periods
K = len(num)     # Number of generator types

# Initialize the problem
problem = pulp.LpProblem("Power_Station", pulp.LpMinimize)

# Decision variables: numon[k][t] and x[k][t]
numon = [[pulp.LpVariable(f'numon_{k}_{t}', lowBound=0, upBound=num[k], cat='Integer') for t in range(T)] for k in range(K)]
x = [[pulp.LpVariable(f'x_{k}_{t}', lowBound=0, cat='Continuous') for t in range(T)] for k in range(K)]

# Objective function
problem += pulp.lpSum([
    pulp.lpSum([
        numon[k][t] * runcost[k] + x[k][t] * extracost[k] + startcost[k] * pulp.lpSum([numon[k][t] > numon[k][t-1] if t > 0 else numon[k][t] for k in range(K)]) 
        for t in range(T)
    ]) 
    for k in range(K)
])

# Constraints
for t in range(T):
    # Meet the demand in each period
    problem += pulp.lpSum([numon[k][t] * minlevel[k] + x[k][t] for k in range(K)]) >= demand[t]
    
    for k in range(K):
        # Constraints for the generation above minlevel
        problem += x[k][t] <= (maxlevel[k] - minlevel[k]) * numon[k][t]

# Solve the problem
problem.solve()

# Collect results
numon_result = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]

# Output the results
solution = {
    "numon": numon_result
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')