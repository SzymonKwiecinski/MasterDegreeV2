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

# Problem Definition
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((k, t) for k in range(K) for t in range(T)), lowBound=0, upBound=None, cat='Continuous')
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(
    x[k, t] * data['runcost'][k] +
    (data['minlevel'][k] - x[k, t]) * data['extracost'][k] +
    y[k, t] * data['startcost'][k]
    for k in range(K) for t in range(T)
), "Total Cost"

# Constraints

# Demand constraint
for t in range(T):
    problem += (
        pulp.lpSum(x[k, t] * data['minlevel'][k] for k in range(K)) +
        pulp.lpSum((data['maxlevel'][k] - x[k, t]) for k in range(K)) >= data['demand'][t],
        f"Demand_Constraint_{t}"
    )

# Generation limits
for k in range(K):
    for t in range(T):
        problem += (x[k, t] * data['minlevel'][k] <= pulp.lpSum(g for g in range(data['maxlevel'][k]))), f"Gen_Limits_{k}_{t}"

# Number of generators constraints
for k in range(K):
    for t in range(T):
        problem += (0 <= x[k, t] <= data['num'][k]), f"Num_Generators_{k}_{t}"

# Start-up constraints
for k in range(K):
    for t in range(1, T):
        problem += (y[k, t] >= x[k, t] - x[k, t-1]), f"Start_Up_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')