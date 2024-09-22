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

# Parameters
T = len(data['demand'])
K = len(data['num'])

# Indices
time_periods = range(T)
generators = range(K)

# Problem
problem = pulp.LpProblem("Power_Generation_Planning", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (generators, time_periods), cat='Binary')
y = pulp.LpVariable.dicts("y", (generators, time_periods), lowBound=0)
z = pulp.LpVariable.dicts("z", (generators, time_periods), cat='Binary')

# Objective function
problem += pulp.lpSum([
    data['runcost'][k] * x[k][t] +
    data['extracost'][k] * (y[k][t] - data['minlevel'][k] * x[k][t]) +
    data['startcost'][k] * z[k][t]
    for k in generators for t in time_periods
])

# Constraints
# Demand satisfaction
for t in time_periods:
    problem += pulp.lpSum([y[k][t] for k in generators]) >= data['demand'][t], f"demand_constraint_{t}"

# Generation limits
for k in generators:
    for t in time_periods:
        problem += data['minlevel'][k] * x[k][t] <= y[k][t], f"min_level_constraint_{k}_{t}"
        problem += y[k][t] <= data['maxlevel'][k] * x[k][t], f"max_level_constraint_{k}_{t}"
        problem += x[k][t] <= data['num'][k], f"max_num_constraint_{k}_{t}"

# Start-up constraints
for k in generators:
    problem += z[k][0] >= x[k][0], f"startup_first_period_{k}"
    for t in range(1, T):
        problem += z[k][t] >= x[k][t] - x[k][t-1], f"startup_constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')