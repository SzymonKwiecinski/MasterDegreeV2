import pulp

# Load data
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

T = len(demand)  # Number of time periods
K = len(num)     # Number of generator types

# Initialize the problem
problem = pulp.LpProblem('GeneratorCommitment', pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts('numon', ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Integer')
level = pulp.LpVariable.dicts('level', ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
startup = pulp.LpVariable.dicts('startup', ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective function
problem += pulp.lpSum(
    runcost[k] * numon[k, t] +
    extracost[k] * level[k, t] +
    startcost[k] * startup[k, t]
    for k in range(K)
    for t in range(T)
)

# Constraints
for t in range(T):
    # Meet demand
    problem += pulp.lpSum(
        minlevel[k] * numon[k, t] + level[k, t]
        for k in range(K)
    ) >= demand[t]

    for k in range(K):
        # Limits on the number of units
        problem += numon[k, t] <= num[k]

        # Operation levels
        problem += level[k, t] <= (maxlevel[k] - minlevel[k]) * numon[k, t]

        # Startup condition
        if t == 0:
            problem += startup[k, t] == numon[k, t]
        else:
            problem += startup[k, t] >= numon[k, t] - numon[k, t - 1]

# Solve the problem
problem.solve()

# Extract results
numon_result = [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]

# Print the results
output = {
    'numon': numon_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')