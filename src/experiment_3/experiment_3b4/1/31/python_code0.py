import pulp

# Data
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Extract data
demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

# Sets
T = range(len(demand))
K = range(len(num))

# Problem
problem = pulp.LpProblem("Generator_Scheduling", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((k,t) for k in K for t in T), cat='Integer', lowBound=0)
y = pulp.LpVariable.dicts("y", ((k,t) for k in K for t in T), cat='Integer', lowBound=0)
p = pulp.LpVariable.dicts("p", ((k,t) for k in K for t in T), cat='Continuous', lowBound=0)

# Objective Function
problem += pulp.lpSum(
    runcost[k] * x[k, t] + extracost[k] * p[k, t] + startcost[k] * y[k, t]
    for k in K for t in T
)

# Constraints
for t in T:
    problem += pulp.lpSum(minlevel[k] * x[k, t] + p[k, t] for k in K) >= demand[t], f"Demand_Constraint_{t}"

for k in K:
    for t in T:
        problem += p[k, t] <= (maxlevel[k] - minlevel[k]) * x[k, t], f"Power_Output_Constraint_{k}_{t}"

for k in K:
    for t in T[1:]:  # Starting from 1 since t-1 is needed
        problem += x[k, t] - x[k, t-1] <= y[k, t], f"Startup_Constraint_{k}_{t}"

for k in K:
    for t in T:
        problem += x[k, t] <= num[k], f"Max_Generators_Constraint_{k}_{t}"

# Solve
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')