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

# Parameters
T = len(data['demand'])
K = len(data['num'])
M = 10000  # sufficiently large constant

# Problem
problem = pulp.LpProblem("Electricity_Generation_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    data['runcost'][k] * numon[(k, t)] +
    data['extracost'][k] * (level[(k, t)] - data['minlevel'][k]) * numon[(k, t)] +
    data['startcost'][k] * y[(k, t)]
    for k in range(K) for t in range(T)
)

# Constraints
# Demand Satisfaction
for t in range(T):
    problem += pulp.lpSum(level[(k, t)] for k in range(K)) >= data['demand'][t]

# Operational Level Limits
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[(k, t)] <= level[(k, t)]
        problem += level[(k, t)] <= data['maxlevel'][k] * numon[(k, t)]

# Binary Startup Decision
for k in range(K):
    for t in range(T):
        problem += level[(k, t)] <= M * y[(k, t)]

# Generator Availability
for k in range(K):
    problem += pulp.lpSum(numon[(k, t)] for t in range(T)) <= data['num'][k]

# Solve the problem
problem.solve()

# Output
solution = {"numon": [[pulp.value(numon[(k, t)]) for t in range(T)] for k in range(K)]}
print("Solution: ", solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')