import pulp
import numpy as np
import json

# Load the data
data = json.loads("{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}")

demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

T = len(demand)
K = len(num)

# Create the problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Define decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')
output = pulp.LpVariable.dicts("output", (range(K), range(T)), lowBound=0)
startup = pulp.LpVariable.dicts("startup", (range(K), range(T)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(
    runcost[k] * numon[k][t] +
    extracost[k] * (output[k][t] - minlevel[k] * numon[k][t]) +
    startcost[k] * startup[k][t]
    for k in range(K) for t in range(T)
)

# Constraints
for t in range(T):
    problem += pulp.lpSum(output[k][t] for k in range(K)) >= demand[t]

for k in range(K):
    for t in range(T):
        problem += minlevel[k] * numon[k][t] <= output[k][t]
        problem += output[k][t] <= maxlevel[k] * numon[k][t]

for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= num[k]

for k in range(K):
    for t in range(1, T):
        problem += startup[k][t] >= numon[k][t] - numon[k][t-1]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')