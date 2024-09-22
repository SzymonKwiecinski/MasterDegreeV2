import pulp
import json

# Data input
data = {'demand': [15000, 30000, 25000, 40000, 27000], 
        'num': [12, 10, 5], 
        'minlevel': [850, 1250, 1500], 
        'maxlevel': [2000, 1750, 4000], 
        'runcost': [1000, 2600, 3000], 
        'extracost': [2.0, 1.3, 3.0], 
        'startcost': [2000, 1000, 500]}

T = len(data['demand'])
K = len(data['num'])

# Model
problem = pulp.LpProblem("PowerGeneration", pulp.LpMinimize)

# Variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, upBound=None, cat='Integer')
power = pulp.LpVariable.dicts("power", (range(K), range(T)), lowBound=0, upBound=None)

# Objective function
total_cost = pulp.lpSum([
    (data['startcost'][k] * pulp.lpIndicator(numon[k][t] > 0)) + 
    (data['runcost'][k] * numon[k][t]) + 
    (data['extracost'][k] * power[k][t]) 
    for k in range(K) for t in range(T)
])
problem += total_cost

# Constraints
for t in range(T):
    problem += pulp.lpSum([power[k][t] for k in range(K)]) >= data['demand'][t]
    problem += pulp.lpSum([numon[k][t] for k in range(K)]) <= data['num'][k]

for k in range(K):
    for t in range(T):
        problem += power[k][t] >= data['minlevel'][k] * numon[k][t]
        problem += power[k][t] <= data['maxlevel'][k] * numon[k][t]

# Solve the problem
problem.solve()

# Prepare the output
numon_result = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]

# Print output
output = {"numon": numon_result}
print(json.dumps(output))

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')