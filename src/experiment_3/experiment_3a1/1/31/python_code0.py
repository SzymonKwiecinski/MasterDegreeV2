import pulp
import json

# Input data
data = json.loads('{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}')

# Parameters
T = len(data['demand'])  # Number of time periods
K = len(data['num'])      # Number of generator types

# Create a LP problem
problem = pulp.LpProblem("PowerGeneration", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", (k for k in range(K) for t in range(T)), cat='Binary')

# Objective function
problem += pulp.lpSum(data['startcost'][k] * y[k, t] for k in range(K) for t in range(T)) + \
           pulp.lpSum(data['runcost'][k] * numon[k, t] for k in range(K) for t in range(T)) + \
           pulp.lpSum(data['extracost'][k] * pulp.lpSum(numon[k, t] - data['minlevel'][k] for t in range(T)) for k in range(K))

# Constraints
# Demand satisfaction
for t in range(T):
    problem += pulp.lpSum(numon[k, t] for k in range(K)) >= data['demand'][t]

# Generator capacity
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * y[k, t] <= numon[k, t]
        problem += numon[k, t] <= data['maxlevel'][k] * y[k, t]

# Generator availability
for k in range(K):
    for t in range(T):
        problem += numon[k, t] <= data['num'][k]

# Solve the problem
problem.solve()

# Output results
numon_result = [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]
print(f'Output: {{ "numon": {numon_result} }}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')