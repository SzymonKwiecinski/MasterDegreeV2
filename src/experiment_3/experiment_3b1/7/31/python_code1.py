import pulp
import json

# Data in JSON format
data = json.loads('{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}')

# Extracting data
T = len(data['demand'])
K = len(data['num'])
demand_t = data['demand']
num_k = data['num']
minlevel_k = data['minlevel']
maxlevel_k = data['maxlevel']
runcost_k = data['runcost']
extracost_k = data['extracost']
startcost_k = data['startcost']

# Create the optimization problem
problem = pulp.LpProblem("Power_Generation_Optimization", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Integer')
output = pulp.LpVariable.dicts("output", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
start = pulp.LpVariable.dicts("start", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective function
problem += pulp.lpSum(runcost_k[k] * numon[(k, t)] + startcost_k[k] * start[(k, t)] + 
                       extracost_k[k] * (output[(k, t)] - minlevel_k[k]) 
                       for k in range(K) for t in range(T) 
                       if pulp.lpSum(output[(k, t)]) > minlevel_k[k]), "Total_Cost"

# Constraints
for t in range(T):
    problem += pulp.lpSum(output[(k, t)] for k in range(K)) >= demand_t[t], f"Demand_Constraint_{t}"

for k in range(K):
    for t in range(T):
        problem += output[(k, t)] == minlevel_k[k] * numon[(k, t)] + \
                   pulp.lpSum(m * numon[(k, t)] for m in range(1, maxlevel_k[k] - minlevel_k[k] + 1)), f"Output_Constraint_{k}_{t}"
        
        problem += numon[(k, t)] <= num_k[k], f"Generator_Limit_{k}_{t}"
        
        problem += output[(k, t)] <= maxlevel_k[k] * numon[(k, t)], f"Max_Output_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Output the result
numon_result = [[pulp.value(numon[(k, t)]) for t in range(T)] for k in range(K)]
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Output (numon): {numon_result}')