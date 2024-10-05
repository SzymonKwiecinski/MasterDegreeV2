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
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Integer')
x = pulp.LpVariable.dicts("x", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['runcost'][k] * numon[k, t] +
                      data['extracost'][k] * max(0, x[k, t] - data['minlevel'][k]) +
                      data['startcost'][k] * y[k, t]
                      for k in range(K) for t in range(T))

# Constraints

# Demand Satisfaction Constraint
for t in range(T):
    problem += pulp.lpSum(x[k, t] for k in range(K)) == data['demand'][t]

# Generation Level Constraints
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k, t] <= x[k, t]
        problem += x[k, t] <= data['maxlevel'][k] * numon[k, t]

# Linking Start-Up Decision
for k in range(K):
    for t in range(1, T):
        problem += y[k, t] >= numon[k, t] - numon.get((k, t-1), 0)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print decision variables (for demonstration purposes, although not requested)
numon_output = {(k, t): pulp.value(numon[k, t]) for k in range(K) for t in range(T)}
print("numon:", numon_output)