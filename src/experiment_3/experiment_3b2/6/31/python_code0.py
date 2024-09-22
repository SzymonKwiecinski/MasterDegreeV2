import pulp
import json

# Data from the provided JSON
data = json.loads("{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}")

# Extract data
demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

T = len(demand)  # Number of time periods
K = len(num)     # Number of types of generators

# Create a linear programming problem
problem = pulp.LpProblem("Power_Generation_Scheduling", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')
level = pulp.LpVariable.dicts("level", (range(K), range(T)), lowBound=0)
start = pulp.LpVariable.dicts("start", (range(K), range(T)), cat='Binary')

# Objective function
problem += pulp.lpSum(runcost[k] * numon[k][t] + extracost[k] * level[k][t] * numon[k][t] + startcost[k] * start[k][t]
                       for k in range(K) for t in range(T))

# Demand satisfaction constraints
for t in range(T):
    problem += pulp.lpSum((minlevel[k] + level[k][t]) * numon[k][t] for k in range(K)) >= demand[t]

# Capacity constraints
for k in range(K):
    for t in range(T):
        problem += level[k][t] <= (maxlevel[k] - minlevel[k]) * numon[k][t]

# Number of operational units constraints
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= num[k]

# Startup constraints
for k in range(K):
    for t in range(1, T):
        problem += start[k][t] >= numon[k][t] - numon[k][t - 1]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')