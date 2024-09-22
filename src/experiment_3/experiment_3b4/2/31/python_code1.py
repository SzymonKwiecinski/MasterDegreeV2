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

# Problem
problem = pulp.LpProblem("Power_Generation_Scheduling", pulp.LpMinimize)

# Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Integer')
genabove = pulp.LpVariable.dicts("genabove", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
startup = pulp.LpVariable.dicts("startup", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    numon[k, t] * data['runcost'][k] +
    genabove[k, t] * data['extracost'][k] +
    startup[k, t] * data['startcost'][k]
    for k in range(K) for t in range(T)
)

# Constraints
# Demand satisfaction
for t in range(T):
    problem += pulp.lpSum(
        numon[k, t] * data['minlevel'][k] + genabove[k, t]
        for k in range(K)
    ) >= data['demand'][t]

# Generation limits
for k in range(K):
    for t in range(T):
        problem += genabove[k, t] <= numon[k, t] * (data['maxlevel'][k] - data['minlevel'][k])

# Availability of generators
for k in range(K):
    for t in range(T):
        problem += numon[k, t] <= data['num'][k]

# Startup cost modeling
for k in range(K):
    for t in range(1, T):
        problem += startup[k, t] >= (numon[k, t] - numon[k, t-1]) / data['num'][k]
    # Initial startup
    problem += startup[k, 0] >= numon[k, 0] / data['num'][k] if data['num'][k] > 0 else 0

# Solve
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')