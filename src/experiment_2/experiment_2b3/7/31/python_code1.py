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

# Indices
T = len(data['demand'])
K = len(data['num'])

# Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, upBound=data['num'][k], cat=pulp.LpInteger)
output = pulp.LpVariable.dicts("output", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat=pulp.LpContinuous)
start = pulp.LpVariable.dicts("start", ((k, t) for k in range(K) for t in range(T)), cat=pulp.LpBinary)

# Problem
problem = pulp.LpProblem("Minimize Costs", pulp.LpMinimize)

# Objective
problem += pulp.lpSum(data['runcost'][k] * numon[k, t] + 
                      data['extracost'][k] * (output[k, t] - data['minlevel'][k] * numon[k, t]) +
                      data['startcost'][k] * start[k, t]
                      for k in range(K) for t in range(T))

# Constraints
for t in range(T):
    problem += pulp.lpSum(output[k, t] for k in range(K)) >= data['demand'][t]
    for k in range(K):
        problem += output[k, t] <= data['maxlevel'][k] * numon[k, t]
        problem += output[k, t] >= data['minlevel'][k] * numon[k, t]
        if t == 0:
            problem += numon[k, t] <= data['num'][k]
            problem += start[k, t] >= numon[k, t]
        else:
            problem += start[k, t] >= numon[k, t] - numon[k, t-1]

# Solve
problem.solve()

# Output
result = {
    "numon": [[int(numon[k, t].varValue) for t in range(T)] for k in range(K)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')