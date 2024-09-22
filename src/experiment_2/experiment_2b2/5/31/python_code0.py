import pulp

# Load data
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Constants
T = len(data['demand'])
K = len(data['num'])

# Problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", ((k, t) for k in range(K) for t in range(T)), cat='Binary')  # 1 if generator k operates at time t
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')  # Power above min level
z = pulp.LpVariable.dicts("z", ((k, t) for k in range(K) for t in range(T)), cat='Binary')  # 1 if generator k is started at time t

# Objective function: cost minimization
problem += pulp.lpSum([
    x[k, t] * data['runcost'][k] +
    y[k, t] * data['extracost'][k] +
    z[k, t] * data['startcost'][k]
    for k in range(K) for t in range(T)
])

# Constraints
for t in range(T):
    # Demand constraint
    problem += pulp.lpSum([
        x[k, t] * data['minlevel'][k] + y[k, t]
        for k in range(K)
    ]) >= data['demand'][t]

    for k in range(K):
        # Number of generators constraint
        problem += x[k, t] <= data['num'][k]

        # Power output must be between min and max
        problem += y[k, t] <= x[k, t] * (data['maxlevel'][k] - data['minlevel'][k])

        # Start-up constraint
        if t > 0:
            problem += z[k, t] >= x[k, t] - x[k, t - 1]
        else:
            problem += z[k, t] >= x[k, t]

# Solve the problem
problem.solve()

# Retrieve the results
numon = [[int(x[k, t].varValue) for t in range(T)] for k in range(K)]

# Output
solution = {
    "numon": numon
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')