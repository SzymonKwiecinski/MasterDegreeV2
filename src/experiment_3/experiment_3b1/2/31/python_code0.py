import pulp
import json

# Load data from the provided JSON
data = json.loads("{'demand': [15000, 30000, 25000, 40000, 27000], 'num': [12, 10, 5], 'minlevel': [850, 1250, 1500], 'maxlevel': [2000, 1750, 4000], 'runcost': [1000, 2600, 3000], 'extracost': [2.0, 1.3, 3.0], 'startcost': [2000, 1000, 500]}")

# Extract data
demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

# Define indices
T = len(demand)
K = len(num)

# Define the problem
problem = pulp.LpProblem("Minimize_Generation_Cost", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, upBound=None, cat='Integer')
x = pulp.LpVariable.dicts("x", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(runcost[k] * numon[(k, t)] + extracost[k] * x[(k, t)] + startcost[k] * y[(k, t)] for k in range(K) for t in range(T))

# Constraints
for t in range(T):
    problem += pulp.lpSum(numon[(k, t)] * minlevel[k] + x[(k, t)] for k in range(K)) >= demand[t]

for k in range(K):
    for t in range(T):
        problem += numon[(k, t)] <= num[k]

for k in range(K):
    for t in range(T):
        problem += numon[(k, t)] * minlevel[k] + x[(k, t)] <= numon[(k, t)] * maxlevel[k]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')