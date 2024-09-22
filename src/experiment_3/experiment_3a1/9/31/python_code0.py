import pulp
import json

# Data from the given JSON format
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
T = len(data['demand'])  # Total number of time periods
K = len(data['num'])      # Total number of generator types

# Create the LP problem
problem = pulp.LpProblem("Generator_Scheduling", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, upBound=None, cat='Integer')
level = pulp.LpVariable.dicts("level", (range(K), range(T)), lowBound=0, upBound=None)
is_on = pulp.LpVariable.dicts("is_on", (range(K), range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['runcost'][k] * numon[k][t] +
                       data['extracost'][k] * (level[k][t] - data['minlevel'][k]) * numon[k][t] +
                       data['startcost'][k] * is_on[k][t]
                       for k in range(K) for t in range(T))

# Constraints
# Demand satisfaction
for t in range(T):
    problem += pulp.lpSum(level[k][t] for k in range(K)) >= data['demand'][t]

# Operational level bounds
for k in range(K):
    for t in range(T):
        problem += level[k][t] >= data['minlevel'][k] * is_on[k][t]
        problem += level[k][t] <= data['maxlevel'][k] * is_on[k][t]

# Generators on/off
for k in range(K):
    for t in range(T):
        problem += level[k][t] <= data['maxlevel'][k] * is_on[k][t]

# Number of generators
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= data['num'][k] * is_on[k][t]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')