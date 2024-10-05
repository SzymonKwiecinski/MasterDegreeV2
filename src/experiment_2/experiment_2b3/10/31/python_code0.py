import pulp

# Data from the problem description
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

T = len(demand)
K = len(num)

# Create a problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), 
                              lowBound=0, cat=pulp.LpInteger)
additional_power = pulp.LpVariable.dicts("additional_power", ((k, t) for k in range(K) for t in range(T)), 
                                         lowBound=0, cat=pulp.LpContinuous)
startup = pulp.LpVariable.dicts("startup", ((k, t) for k in range(K) for t in range(T)), 
                                cat=pulp.LpBinary)

# Objective function
total_cost = pulp.lpSum(
    runcost[k] * numon[(k, t)] + 
    extracost[k] * additional_power[(k, t)] + 
    startcost[k] * startup[(k, t)]
    for k in range(K) for t in range(T)
)
problem += total_cost

# Constraints
# Demand constraints
for t in range(T):
    problem += pulp.lpSum(minlevel[k] * numon[(k, t)] + additional_power[(k, t)] for k in range(K)) >= demand[t]

# Generator constraints
for k in range(K):
    for t in range(T):
        problem += additional_power[(k, t)] <= (maxlevel[k] - minlevel[k]) * numon[(k, t)]
        problem += numon[(k, t)] <= num[k]
        if t == 0:
            problem += numon[(k, t)] <= num[k] * startup[(k, t)]
        else:
            problem += numon[(k, t)] <= num[k] * (startup[(k, t)] + numon[(k, t-1)])

# Solve the problem
problem.solve()

# Prepare the output
solution = {
    "numon": [[pulp.value(numon[(k, t)]) for t in range(T)] for k in range(K)]
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')