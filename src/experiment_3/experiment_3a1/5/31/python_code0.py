import pulp
import json

# Load the data from JSON format
data = json.loads('{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}')

# Extract data for easier access
demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']
T = len(demand)
K = len(num)

# Create the optimization problem
problem = pulp.LpProblem("PowerGeneration", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, upBound=None, cat='Integer')
power = pulp.LpVariable.dicts("power", ((k, t) for k in range(K) for t in range(T)), lowBound=0, upBound=None)
startup = pulp.LpVariable.dicts("startup", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(runcost[k] * numon[k, t] + 
                      extracost[k] * (power[k, t] - minlevel[k]) * numon[k, t] + 
                      startup[k, t] * startcost[k] 
                      for k in range(K) for t in range(T))

# Constraints

# Demand Satisfaction
for t in range(T):
    problem += pulp.lpSum(power[k, t] for k in range(K)) == demand[t]

# Power Output Levels
for k in range(K):
    for t in range(T):
        problem += minlevel[k] * numon[k, t] <= power[k, t]
        problem += power[k, t] <= maxlevel[k] * numon[k, t]

# Number of Running Generators
for k in range(K):
    for t in range(T):
        problem += numon[k, t] <= num[k]

# Generate Binary Startup Variable
for k in range(K):
    for t in range(1, T):  # Start from t=1 since t=0 is not defined
        problem += startup[k, t] >= numon[k, t] - numon[k, t-1]

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')