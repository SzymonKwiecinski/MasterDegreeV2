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

# Indices
T = len(data['demand'])
K = len(data['num'])

# Initialize the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
z = pulp.LpVariable.dicts("z", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective function
problem += pulp.lpSum(
    data['runcost'][k] * x[k, t] + 
    data['extracost'][k] * y[k, t] + 
    data['startcost'][k] * z[k, t]
    for k in range(K) for t in range(T)
)

# Constraints
# Demand Satisfaction
for t in range(T):
    problem += pulp.lpSum(data['minlevel'][k] * x[k, t] + y[k, t] for k in range(K)) >= data['demand'][t]

# Generator Operating Limits
for k in range(K):
    for t in range(T):
        problem += y[k, t] <= (data['maxlevel'][k] - data['minlevel'][k]) * x[k, t]

# Number of Generators
for k in range(K):
    for t in range(T):
        problem += x[k, t] <= data['num'][k]

# Startup Cost
for k in range(K):
    for t in range(1, T):
        problem += z[k, t] >= x[k, t] - x[k, t-1]

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')