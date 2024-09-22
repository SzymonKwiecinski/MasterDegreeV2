import json
import pulp

data = {'demand': [15000, 30000, 25000, 40000, 27000], 
        'num': [12, 10, 5], 
        'minlevel': [850, 1250, 1500], 
        'maxlevel': [2000, 1750, 4000], 
        'runcost': [1000, 2600, 3000], 
        'extracost': [2.0, 1.3, 3.0], 
        'startcost': [2000, 1000, 500]}

demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

# Define the problem
problem = pulp.LpProblem("Power_Generation", pulp.LpMinimize)

K = len(num)  # Number of generator types
T = len(demand)  # Number of time periods

# Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')
power = pulp.LpVariable.dicts("power", (range(K), range(T)), lowBound=0)

# Objective function
total_cost = pulp.lpSum(startcost[k] * pulp.lpSum(numon[k][t] for t in range(T)) + 
                         runcost[k] * numon[k][t] + 
                         extracost[k] * (power[k][t] - minlevel[k]) * numon[k][t]
                         for k in range(K) for t in range(T))

problem += total_cost

# Constraints
for t in range(T):
    # Demand must be satisfied
    problem += pulp.lpSum(power[k][t] for k in range(K)) >= demand[t]
    
    # Each generator's power output must respect min and max levels
    for k in range(K):
        problem += power[k][t] >= minlevel[k] * numon[k][t]
        problem += power[k][t] <= maxlevel[k] * numon[k][t]

# Ensuring the number of generators on does not exceed available units
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= num[k]

# Solve the problem
problem.solve()

# Output the results
numon_output = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]
result = {"numon": numon_output}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')