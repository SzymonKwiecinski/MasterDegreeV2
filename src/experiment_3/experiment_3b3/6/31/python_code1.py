import pulp

# Data from the problem
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Parameters
T = len(data['demand'])
K = len(data['num'])
demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

# Problem
problem = pulp.LpProblem("Generator_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat=pulp.LpInteger)
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat=pulp.LpContinuous)
start = pulp.LpVariable.dicts("start", ((k, t) for k in range(K) for t in range(T)), lowBound=0, upBound=1, cat=pulp.LpBinary)

# Objective Function
problem += pulp.lpSum(
    runcost[k] * numon[k, t] + startcost[k] * start[k, t] +
    extracost[k] * (level[k, t] - minlevel[k]) * numon[k, t] 
    for k in range(K) for t in range(T)
), 'Total_Cost'

# Constraints
for t in range(T):
    problem += pulp.lpSum(level[k, t] for k in range(K)) == demand[t], f"Demand_Fulfillment_t{t}"

for k in range(K):
    for t in range(T):
        problem += minlevel[k] * numon[k, t] <= level[k, t], f"Min_Level_k{k}_t{t}"
        problem += level[k, t] <= maxlevel[k] * numon[k, t], f"Max_Level_k{k}_t{t}"
        problem += numon[k, t] <= num[k], f"Max_Availability_k{k}_t{t}"
        problem += start[k, t] <= numon[k, t], f"Start_Consistency_k{k}_t{t}"

# Solve the problem
problem.solve()

# Extract the solution
solution = {
    'numon': [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]
}

print("Output:", solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')