import pulp
import json

# Data input in JSON format
data = json.loads('{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}')

# Sets
T = len(data['demand'])  # Number of time periods
K = len(data['num'])      # Number of generator types

# Parameters
demand = data['demand']
num_k = data['num']
minlevel_k = data['minlevel']
maxlevel_k = data['maxlevel']
runcost_k = data['runcost']
extracost_k = data['extracost']
startcost_k = data['startcost']

# Decision Variables
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')
level = pulp.LpVariable.dicts("level", (range(K), range(T)), lowBound=0)
start = pulp.LpVariable.dicts("start", range(K), cat='Binary')

# Objective Function
problem += pulp.lpSum(runcost_k[k] * numon[k][t] + startcost_k[k] * start[k] +
                       extracost_k[k] * (level[k][t] - minlevel_k[k]) * numon[k][t]
                       for k in range(K) for t in range(T)), "Total_Cost"

# Constraints
# Demand Constraint
for t in range(T):
    problem += pulp.lpSum(level[k][t] for k in range(K)) == demand[t], f"Demand_Constraint_{t+1}"

# Generator Operating Levels
for k in range(K):
    for t in range(T):
        problem += minlevel_k[k] * numon[k][t] <= level[k][t], f"Min_Operating_Level_{k+1}_{t+1}"
        problem += level[k][t] <= maxlevel_k[k] * numon[k][t], f"Max_Operating_Level_{k+1}_{t+1}"

# Availability of Generators
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= num_k[k], f"Availability_{k+1}_{t+1}"

# Startup Constraint
for k in range(K):
    for t in range(1, T):  # Start from 2nd time period
        problem += start[k] >= numon[k][t] - numon[k][t-1], f"Startup_Constraint_{k+1}_{t+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')