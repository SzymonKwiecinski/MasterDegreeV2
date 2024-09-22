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

T = len(data['demand'])
K = len(data['num'])

# Initialize the problem
problem = pulp.LpProblem("Generator_Scheduling", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat=pulp.LpInteger)
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), cat=pulp.LpBinary)
p = pulp.LpVariable.dicts("p", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function
problem += pulp.lpSum(
    x[k, t] * data['runcost'][k] + 
    p[k, t] * data['extracost'][k] + 
    y[k, t] * data['startcost'][k]
    for k in range(K) for t in range(T)
)

# Constraints
# Demand satisfaction
for t in range(T):
    problem += pulp.lpSum(x[k, t] * data['minlevel'][k] + p[k, t] for k in range(K)) >= data['demand'][t]

# Power output limits
for k in range(K):
    for t in range(T):
        problem += p[k, t] <= x[k, t] * (data['maxlevel'][k] - data['minlevel'][k])
        problem += x[k, t] <= data['num'][k]

# Start-up conditions
for k in range(K):
    for t in range(1, T):
        problem += y[k, t] >= x[k, t] - x[k, t - 1]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')