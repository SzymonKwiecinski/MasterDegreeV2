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

T = len(data['demand'])  # Number of time periods
K = len(data['num'])      # Number of generator types

# Define the problem
problem = pulp.LpProblem("PowerGenerationOptimization", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), 0, None, pulp.LpInteger)
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), 0, None)
startup = pulp.LpVariable.dicts("startup", ((k, t) for k in range(K) for t in range(T)), 0, 1, pulp.LpBinary)

# Objective Function
problem += pulp.lpSum(
    data['runcost'][k] * numon[k, t] +
    data['extracost'][k] * (level[k, t] - data['minlevel'][k]) * numon[k, t] +
    data['startcost'][k] * startup[k, t]
    for k in range(K) for t in range(T)
)

# Constraints
# Demand Satisfaction
for t in range(T):
    problem += pulp.lpSum(level[k, t] for k in range(K)) >= data['demand'][t]

# Operational Level Limits
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k, t] <= level[k, t]
        problem += level[k, t] <= data['maxlevel'][k] * numon[k, t]

# Generator Availability
for k in range(K):
    problem += pulp.lpSum(numon[k, t] for t in range(T)) <= data['num'][k]

# Startup Decision
for k in range(K):
    for t in range(T):
        problem += level[k, t] <= data['maxlevel'][k] * startup[k, t]

# Solve the problem
problem.solve()

# Output the results
numon_output = [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')