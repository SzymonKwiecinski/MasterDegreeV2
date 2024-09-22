import pulp
import json

# Data
data_json = '''{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}'''
data = json.loads(data_json)

# Indices
T = len(data['demand'])
K = len(data['num'])

# Create the problem
problem = pulp.LpProblem("MinimizeTotalCost", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(1, T + 1)), lowBound=0, upBound=[data['num'][k] for k in range(K)], cat='Integer')
output = pulp.LpVariable.dicts("output", (range(K), range(1, T + 1)), lowBound=0, cat='Continuous')
startup = pulp.LpVariable.dicts("startup", (range(K), range(1, T + 1)), cat='Binary')

# Objective Function
problem += pulp.lpSum(numon[k][t] * data['runcost'][k] + output[k][t] * data['extracost'][k] + startup[k][t] * data['startcost'][k] for k in range(K) for t in range(1, T + 1))

# Constraints

# Demand satisfaction
for t in range(1, T + 1):
    problem += pulp.lpSum(numon[k][t] * data['minlevel'][k] + output[k][t] for k in range(K)) >= data['demand'][t - 1]

# Output limits
for k in range(K):
    for t in range(1, T + 1):
        problem += output[k][t] <= numon[k][t] * (data['maxlevel'][k] - data['minlevel'][k])
        problem += output[k][t] >= 0

# Generator availability
for k in range(K):
    for t in range(1, T + 1):
        problem += numon[k][t] <= data['num'][k]

# Startup constraints
for k in range(K):
    for t in range(2, T + 1):
        problem += startup[k][t] >= numon[k][t] - numon[k][t - 1]
    problem += startup[k][1] >= numon[k][1]

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')