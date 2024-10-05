import pulp

# Extracting data
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

# Number of periods and types of generators
T = len(demand)
K = len(num)

# Initialize the problem
problem = pulp.LpProblem("Generator_Optimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("started", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective function
total_cost = (
    pulp.lpSum(runcost[k] * minlevel[k] * x[k, t] + extracost[k] * (pulp.lpSum(x[k, t] * pulp.LpVariable(f"output_{k}_{t}_{i}", lowBound=0, upBound=maxlevel[k]-minlevel[k])) / x[k, t])
               for k in range(K) for t in range(T) for i in range(num[k]))
    + pulp.lpSum(startcost[k] * y[k, t] for k in range(K) for t in range(T))
)
problem += total_cost

# Constraints
for t in range(T):
    problem += pulp.lpSum(x[k, t] * minlevel[k] + pulp.lpSum(x[k, t] * pulp.LpVariable(f"output_{k}_{t}_{i}", lowBound=0, upBound=maxlevel[k]-minlevel[k]))
                          for k in range(K) for i in range(num[k])) >= demand[t], f"Demand_Constraint_{t}"

for k in range(K):
    for t in range(T):
        problem += x[k, t] <= num[k], f"Num_Limit_{k}_{t}"

for k in range(K):
    for t in range(T):
        if t > 0:
            problem += x[k, t] - x[k, t-1] <= num[k] * y[k, t], f"Startup_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Extract results
numon_result = [[int(pulp.value(x[k, t])) for t in range(T)] for k in range(K)]

# Output results
output = {
    "numon": numon_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')