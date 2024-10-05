import pulp

# Data
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

T = len(data['demand'])
K = len(data['num'])

# Initialize the problem
problem = pulp.LpProblem("Power_Station_Scheduling", pulp.LpMinimize)

# Decision variables
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), 0, 1, pulp.LpBinary)
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), 0, None, pulp.LpInteger)
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), 0, None, pulp.LpContinuous)

# Objective function
problem += pulp.lpSum(
    numon[k, t] * data['runcost'][k] + level[k, t] * data['extracost'][k] + y[k, t] * data['startcost'][k]
    for k in range(K) for t in range(T)
)

# Constraints

# Demand Fulfillment
for t in range(T):
    problem += pulp.lpSum(
        numon[k, t] * data['minlevel'][k] + level[k, t]
        for k in range(K)
    ) >= data['demand'][t]

# Generator Limits
for k in range(K):
    for t in range(T):
        problem += numon[k, t] <= data['num'][k]

# Output Level Constraints
for k in range(K):
    for t in range(T):
        problem += level[k, t] <= (data['maxlevel'][k] - data['minlevel'][k]) * numon[k, t]

# Start-up Constraints
for k in range(K):
    for t in range(1, T):
        problem += numon[k, t] <= numon[k, t-1] + y[k, t] * data['num'][k]

# Initial Condition
for k in range(K):
    problem += numon[k, 0] <= y[k, 0] * data['num'][k]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')