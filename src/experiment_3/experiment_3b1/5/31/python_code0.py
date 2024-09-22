import pulp
import json

# Data in json format
data = json.loads('{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}')

# Parameters
demand = data['demand']
num_generators = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

T = len(demand)  # Number of time periods
K = len(num_generators)  # Number of generator types

# Create the problem
problem = pulp.LpProblem("Power_Generation_Optimization", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')
level = pulp.LpVariable.dicts("level", (range(K), range(T)), lowBound=0)
y = pulp.LpVariable.dicts("y", (range(K), range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(startcost[k] * y[k][t] + runcost[k] * numon[k][t] + 
                       extracost[k] * (level[k][t] - minlevel[k]) * numon[k][t]
                       for t in range(T) for k in range(K))

# Constraints
# Demand satisfaction
for t in range(T):
    problem += pulp.lpSum(level[k][t] for k in range(K)) >= demand[t]

# Operating level constraints
for k in range(K):
    for t in range(T):
        problem += (minlevel[k] * numon[k][t] <= level[k][t])
        problem += (level[k][t] <= maxlevel[k] * numon[k][t])

# Generator availability
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= num_generators[k] * y[k][t]

# Binary variable formulation
for k in range(K):
    for t in range(T):
        problem += level[k][t] == 0, "Level_def_{}_{}".format(k, t) if y[k][t] == 0 else ""

# Solve the problem
problem.solve()

# Output the results
numon_output = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]
print("Number of generators on each time period:")
print(numon_output)

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')