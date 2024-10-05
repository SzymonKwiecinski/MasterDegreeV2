import pulp

# Data provided
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Index sets
T = len(data['demand'])
K = len(data['num'])

# Create the problem
problem = pulp.LpProblem("GeneratorSchedule", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), 0, cat=pulp.LpInteger)
output = pulp.LpVariable.dicts("output", ((k, t) for k in range(K) for t in range(T)), 0, cat=pulp.LpContinuous)
start = pulp.LpVariable.dicts("start", ((k, t) for k in range(K) for t in range(T)), 0, 1, cat=pulp.LpBinary)

# Objective function
problem += pulp.lpSum(
    numon[k, t] * data['runcost'][k] +
    output[k, t] * data['extracost'][k] +
    start[k, t] * data['startcost'][k]
    for k in range(K) for t in range(T)
)

# Constraints
# 1. Meet demand for each period
for t in range(T):
    problem += pulp.lpSum(
        numon[k, t] * data['minlevel'][k] + output[k, t]
        for k in range(K)
    ) >= data['demand'][t]

# 2. Respect generator output limits
for k in range(K):
    for t in range(T):
        problem += output[k, t] <= (data['maxlevel'][k] - data['minlevel'][k]) * numon[k, t]

# 3. Limit the number of generators that can be on
for k in range(K):
    for t in range(T):
        problem += numon[k, t] <= data['num'][k]

# 4. Startup logic
for k in range(K):
    for t in range(1, T):
        problem += start[k, t] >= numon[k, t] - numon[k, t-1]

# 5. Initial conditions
for k in range(K):
    problem += start[k, 0] >= numon[k, 0]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')