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

T = len(data['demand'])  # number of periods
K = len(data['num'])     # number of generator types

# Decision Variables
problem = pulp.LpProblem("Power_Generation", pulp.LpMinimize)

numon = [[pulp.LpVariable(f"numon_{k}_{t}", lowBound=0, upBound=data['num'][k], cat='Integer') for t in range(T)] for k in range(K)]
level = [[pulp.LpVariable(f"level_{k}_{t}", lowBound=0) for t in range(T)] for k in range(K)]
startup = [[pulp.LpVariable(f"startup_{k}_{t}", cat='Binary') for t in range(T)] for k in range(K)]

# Objective Function
total_cost = pulp.lpSum([
    pulp.lpSum([
        data['runcost'][k] * numon[k][t] +
        data['extracost'][k] * (level[k][t] - numon[k][t] * data['minlevel'][k]) +
        data['startcost'][k] * startup[k][t]
        for t in range(T)
    ])
    for k in range(K)
])
problem += total_cost

# Constraints
for t in range(T):
    # Meet demand
    problem += pulp.lpSum([level[k][t] for k in range(K)]) >= data['demand'][t]
    
    for k in range(K):
        # Min and max level constraints
        problem += level[k][t] >= numon[k][t] * data['minlevel'][k]
        problem += level[k][t] <= numon[k][t] * data['maxlevel'][k]
        
        # Startup constraints
        if t == 0:
            problem += numon[k][t] <= startup[k][t] * data['num'][k]
        else:
            problem += numon[k][t] - numon[k][t-1] <= startup[k][t] * data['num'][k]

# Solve
problem.solve()

# Extract results
numon_result = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]

# Output
output = {
    "numon": numon_result
}

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
output