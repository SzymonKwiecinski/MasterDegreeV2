import pulp

# Data from JSON
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Sets and Parameters
T = len(data['demand'])  # Number of time periods
K = len(data['num'])  # Number of generator types

# Initialize the LP problem
problem = pulp.LpProblem("Power_Generation_Optimization", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Integer')
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
startup = pulp.LpVariable.dicts("startup", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    data['runcost'][k] * numon[k, t] +
    data['startcost'][k] * startup[k, t] +
    data['extracost'][k] * (level[k, t] - data['minlevel'][k]) * numon[k, t]
    for k in range(K)
    for t in range(T)
), "Total Cost"

# Constraints

# Demand Satisfaction
for t in range(T):
    problem += pulp.lpSum(level[k, t] for k in range(K)) >= data['demand'][t]

# Operational Level Limits
for k in range(K):
    for t in range(T):
        problem += level[k, t] >= data['minlevel'][k] * numon[k, t]
        problem += level[k, t] <= data['maxlevel'][k] * numon[k, t]

# Startup Constraints
for k in range(K):
    for t in range(T):
        problem += level[k, t] <= data['maxlevel'][k] * startup[k, t]

# Number of Generators
for k in range(K):
    for t in range(T):
        problem += numon[k, t] <= data['num'][k]

# Solve the problem
problem.solve()

# Print results
output = {'numon': [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]}
print("Output:", output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')