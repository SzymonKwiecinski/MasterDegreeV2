import pulp
import json

# Data from the JSON format
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Defining parameters
T = len(data['demand'])  # Number of time periods
K = len(data['num'])      # Number of generator types

# Create a problem variable
problem = pulp.LpProblem("Power_Generation_Optimization", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, upBound=None, cat='Integer')
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), lowBound=0, upBound=None)
start = pulp.LpVariable.dicts("start", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['runcost'][k] * numon[(k, t)] + data['startcost'][k] * start[(k, t)] + 
                       data['extracost'][k] * pulp.lpMax(0, level[(k, t)] - data['minlevel'][k]) * numon[(k, t)]
                       for k in range(K) for t in range(T))

# Constraints

# Demand satisfaction
for t in range(T):
    problem += pulp.lpSum(level[(k, t)] for k in range(K)) >= data['demand'][t]

# Generator capacity
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[(k, t)] <= level[(k, t)]
        problem += level[(k, t)] <= data['maxlevel'][k] * numon[(k, t)]

# Generator availability
for k in range(K):
    for t in range(T):
        problem += numon[(k, t)] <= data['num'][k]

# Startup decision
for k in range(K):
    for t in range(T):
        problem += level[(k, t)] <= data['maxlevel'][k] * start[(k, t)]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')