import pulp
import json

# Data input
data = json.loads("{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}")

# Define model
T = len(data['demand'])
K = len(data['num'])
problem = pulp.LpProblem("Power_Generation_Scheduling", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    data['startcost'][k] * y[k, t] + 
    data['runcost'][k] * numon[k, t] +
    data['extracost'][k] * (level[k, t] - data['minlevel'][k]) * numon[k, t] 
    for k in range(K) for t in range(T)
)

# Constraints

# Demand satisfaction
for t in range(T):
    problem += pulp.lpSum(level[k, t] for k in range(K)) == data['demand'][t]

# Operational level constraints
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k, t] <= level[k, t]
        problem += level[k, t] <= data['maxlevel'][k] * numon[k, t]

# Generator operational constraints
for k in range(K):
    for t in range(T):
        problem += numon[k, t] <= data['num'][k] * y[k, t]

# Non-negativity and binary constraints (already handled in variable definitions)

# Solve the problem
problem.solve()

# Output the results
numon_output = [[pulp.value(numon[k, t]) for k in range(K)] for t in range(T)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')