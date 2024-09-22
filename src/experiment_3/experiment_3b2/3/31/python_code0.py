import pulp

# Data from JSON format
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

# Create the LP problem
problem = pulp.LpProblem("Generator_Operation_Optimization", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, upBound=[data['num'][k] for k in range(K)], cat='Integer')
extra = pulp.LpVariable.dicts("extra", (range(K), range(T)), lowBound=0, cat='Continuous')

# Delta variable to track whether any generator of type k starts in period t
delta = pulp.LpVariable.dicts("delta", (range(K), range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['runcost'][k] * numon[k][t] + 
                       data['extracost'][k] * extra[k][t] + 
                       data['startcost'][k] * delta[k][t] 
                       for k in range(K) for t in range(T))

# Constraints
# Demand constraint
for t in range(T):
    problem += pulp.lpSum((numon[k][t] * data['minlevel'][k] + extra[k][t]) for k in range(K)) >= data['demand'][t]

# Bounds on extra production
for k in range(K):
    for t in range(T):
        problem += extra[k][t] <= numon[k][t] * (data['maxlevel'][k] - data['minlevel'][k])

# Generator capacity constraint
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= data['num'][k]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')