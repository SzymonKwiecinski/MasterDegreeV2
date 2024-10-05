import pulp

# Data from JSON
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Extracting data
demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

T = len(demand)
K = len(num)

# Define the problem
problem = pulp.LpProblem("Power_Station_Optimization", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("NumOn", (range(K), range(T)), lowBound=0, cat='Integer')
power_above_min = pulp.LpVariable.dicts("PowerAboveMin", (range(K), range(T)), lowBound=0, cat='Continuous')
startup = pulp.LpVariable.dicts("Startup", (range(K), range(T)), cat='Binary')

# Objective function
total_cost = pulp.lpSum([
    startup[k][t] * startcost[k] 
    + numon[k][t] * runcost[k] 
    + power_above_min[k][t] * extracost[k]
    for k in range(K) for t in range(T)
])

problem += total_cost

# Constraints
for t in range(T):
    # Demand constraint
    problem += pulp.lpSum([
        numon[k][t] * minlevel[k] + power_above_min[k][t]
        for k in range(K)
    ]) >= demand[t]

    for k in range(K):
        # Constraint - maximum units available
        problem += numon[k][t] <= num[k]

        # Constraint - operating within max and min levels
        problem += power_above_min[k][t] <= (numon[k][t] * (maxlevel[k] - minlevel[k]))

        # Startup constraint
        if t == 0:
            problem += startup[k][t] >= numon[k][t]
        else:
            problem += startup[k][t] >= numon[k][t] - numon[k][t-1]

# Solve the problem
problem.solve()

# Preparing the output
output = {
    "numon": [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')