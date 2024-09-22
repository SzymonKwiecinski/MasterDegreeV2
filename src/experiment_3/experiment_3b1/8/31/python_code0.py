import pulp
import json

data = json.loads('{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}')

T = len(data['demand'])  # number of time periods
K = len(data['num'])  # number of types of generating units

# Create the problem
problem = pulp.LpProblem("Power_Generation_Scheduling", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')
level = pulp.LpVariable.dicts("level", (range(K), range(T)), lowBound=0, cat='Continuous')
start = pulp.LpVariable.dicts("start", (range(K), range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['runcost'][k] * numon[k][t] +
                       data['extracost'][k] * pulp.lpSum(level[k][t] - data['minlevel'][k] * numon[k][t]) +
                       data['startcost'][k] * start[k][t]
                       for t in range(T) for k in range(K))

# Constraints
# Demand Satisfaction
for t in range(T):
    problem += pulp.lpSum(level[k][t] for k in range(K)) == data['demand'][t]

# Operational Level Constraints
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k][t] <= level[k][t]
        problem += level[k][t] <= data['maxlevel'][k] * numon[k][t]

# Generator Availability
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= data['num'][k]

# Startup Indicator
for k in range(K):
    for t in range(T):
        problem += level[k][t] <= data['maxlevel'][k] * start[k][t]

# Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')