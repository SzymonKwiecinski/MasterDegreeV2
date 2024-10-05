import pulp

# Load data from the provided JSON
data = {
    "demand": [15000, 30000, 25000, 40000, 27000],
    "num": [12, 10, 5],
    "minlevel": [850, 1250, 1500],
    "maxlevel": [2000, 1750, 4000],
    "runcost": [1000, 2600, 3000],
    "extracost": [2.0, 1.3, 3.0],
    "startcost": [2000, 1000, 500]
}

# Extract data into variables
demand = data['demand']
num_types = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

T = len(demand)
K = len(num_types)

# Create the problem
problem = pulp.LpProblem("Power_Station_Commitment", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Integer')
generated = pulp.LpVariable.dicts("generated", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function
objective = pulp.lpSum([
    numon[k, t] * runcost[k] +
    (generated[k, t] - numon[k, t] * minlevel[k]) * extracost[k] +
    numon[k, t] * startcost[k]
    for k in range(K) for t in range(T)
])

problem += objective

# Constraints
for t in range(T):
    problem += pulp.lpSum([
        generated[k, t] for k in range(K)
    ]) >= demand[t]

for k in range(K):
    for t in range(T):
        problem += numon[k, t] <= num_types[k]
        problem += generated[k, t] <= numon[k, t] * maxlevel[k]
        problem += generated[k, t] >= numon[k, t] * minlevel[k]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "numon": [[int(numon[k, t].varValue) for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')