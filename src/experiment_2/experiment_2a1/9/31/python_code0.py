import pulp
import json

# Input data
data = {'demand': [15000, 30000, 25000, 40000, 27000], 
        'num': [12, 10, 5], 
        'minlevel': [850, 1250, 1500], 
        'maxlevel': [2000, 1750, 4000], 
        'runcost': [1000, 2600, 3000], 
        'extracost': [2.0, 1.3, 3.0], 
        'startcost': [2000, 1000, 500]}

# Extracting data from the input
demand = data['demand']
num_generators = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

# Problem definition
T = len(demand)  # Number of time periods
K = len(num_generators)  # Number of generator types

# Create a problem variable
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, upBound=num_generators, cat='Integer')
power_generated = pulp.LpVariable.dicts("power_generated", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective function
cost = pulp.lpSum(startcost[k] * (numon[k][t] > 0) +
                  runcost[k] * numon[k][t] +
                  extracost[k] * (power_generated[k][t] - minlevel[k]) * numon[k][t] 
                  for k in range(K) for t in range(T))
problem += cost

# Constraints
for t in range(T):
    problem += pulp.lpSum(power_generated[k][t] for k in range(K)) == demand[t]

for k in range(K):
    for t in range(T):
        problem += power_generated[k][t] >= minlevel[k] * numon[k][t]
        problem += power_generated[k][t] <= maxlevel[k] * numon[k][t]

# Solve the problem
problem.solve()

# Output the results
numon_result = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]
result = {
    "numon": numon_result
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')