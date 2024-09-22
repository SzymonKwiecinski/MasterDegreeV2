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

T = len(data['demand'])
K = len(data['num'])

# Define problem
problem = pulp.LpProblem("Power_Generation_Minimization", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("NumOn", ((k, t) for k in range(K) for t in range(T)), 
                              lowBound=0, upBound=None, cat=pulp.LpInteger)
level = pulp.LpVariable.dicts("Level", ((k, t) for k in range(K) for t in range(T)), 
                              lowBound=0, upBound=None, cat=pulp.LpContinuous)
u = pulp.LpVariable.dicts("U", ((k, t) for k in range(K) for t in range(T)), 
                          cat=pulp.LpBinary)

# Objective Function
problem += pulp.lpSum(
    numon[k, t] * data['runcost'][k] +
    level[k, t] * data['extracost'][k] +
    u[k, t] * data['startcost'][k]
    for k in range(K) for t in range(T)
)

# Constraints
# Meet demand in each period
for t in range(T):
    problem += pulp.lpSum(
        numon[k, t] * data['minlevel'][k] + level[k, t]
        for k in range(K)
    ) >= data['demand'][t]

# Generator operational limits
for k in range(K):
    for t in range(T):
        problem += level[k, t] <= numon[k, t] * (data['maxlevel'][k] - data['minlevel'][k])
        problem += numon[k, t] <= data['num'][k]

# Binary start-up condition
for k in range(K):
    for t in range(1, T):
        problem += u[k, t] >= numon[k, t] - numon[k, t - 1]
    # Initial condition for t = 0
    problem += u[k, 0] >= numon[k, 0]

# Solve problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')