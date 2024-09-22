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
problem = pulp.LpProblem("Electricity_Load_Demand", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), cat='Integer')
level = pulp.LpVariable.dicts("level", (range(K), range(T)), lowBound=0)
y = pulp.LpVariable.dicts("y", (range(K), range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    data['startcost'][k] * y[k][t] +
    data['runcost'][k] * numon[k][t] +
    data['extracost'][k] * (level[k][t] - data['minlevel'][k]) * numon[k][t]
    for k in range(K) for t in range(T)
)

# Demand Satisfaction
for t in range(T):
    problem += pulp.lpSum(level[k][t] for k in range(K)) >= data['demand'][t]

# Operational Bounds
for k in range(K):
    for t in range(T):
        problem += level[k][t] >= data['minlevel'][k] * numon[k][t]
        problem += level[k][t] <= data['maxlevel'][k] * numon[k][t]

# Number of Generators On
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= data['num'][k]

# Binary Startup Decision
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= data['num'][k] * y[k][t]

# Level Definition
extra = pulp.LpVariable.dicts("extra", (range(K), range(T)), lowBound=0)
for k in range(K):
    for t in range(T):
        problem += level[k][t] == data['minlevel'][k] * numon[k][t] + extra[k][t]

# Solve the problem
problem.solve()

# Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')