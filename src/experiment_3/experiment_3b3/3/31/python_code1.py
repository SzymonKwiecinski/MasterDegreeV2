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

# Sets
T = range(len(data['demand']))
K = range(len(data['num']))

# Problem
problem = pulp.LpProblem("Power_Generation_Optimization", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in K for t in T), lowBound=0, cat='Integer')
level = pulp.LpVariable.dicts("level", ((k, t) for k in K for t in T), lowBound=0, cat='Continuous')
startup = pulp.LpVariable.dicts("startup", ((k, t) for k in K for t in T), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    data['startcost'][k] * startup[k, t] +
    data['runcost'][k] * numon[k, t] +
    data['extracost'][k] * (pulp.lpSum(pulp.max(level[k, t] - data['minlevel'][k], 0) * numon[k, t]) for k in K for t in T)
)

# Constraints

# Demand Satisfaction
for t in T:
    problem += pulp.lpSum(level[k, t] for k in K) == data['demand'][t]

# Generator Capacity
for k in K:
    for t in T:
        problem += data['minlevel'][k] * numon[k, t] <= level[k, t]
        problem += level[k, t] <= data['maxlevel'][k] * numon[k, t]

# Generator Number
for k in K:
    for t in T:
        problem += numon[k, t] <= data['num'][k]

# Power Level and Startup Relationship
for k in K:
    for t in T:
        problem += level[k, t] <= data['maxlevel'][k] * startup[k, t]

# Solve the problem
problem.solve()

# Output
output = {
    "numon": [[pulp.value(numon[k, t]) for t in T] for k in K]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')