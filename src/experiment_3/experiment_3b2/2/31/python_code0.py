import pulp
import json

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

# Sets and parameters
T = len(data['demand'])  # Number of periods
K = len(data['num'])      # Number of generator types

# Create the LP problem
problem = pulp.LpProblem("PowerStationOperation", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')
pwr = pulp.LpVariable.dicts("pwr", (range(K), range(T), range(max(data['num']))), lowBound=0)
startup = pulp.LpVariable.dicts("startup", (range(K), range(T)), cat='Binary')

# Objective function
problem += pulp.lpSum(
    data['runcost'][k] * numon[k][t] +
    pulp.lpSum(data['extracost'][k] * (pwr[k][t][i] - data['minlevel'][k]) for i in range(data['num'][k])) +
    data['startcost'][k] * startup[k][t]
    for k in range(K) for t in range(T)
)

# Constraints

# Demand Satisfaction
for t in range(T):
    problem += (pulp.lpSum(pwr[k][t][i] for k in range(K) for i in range(data['num'][k])) >= data['demand'][t])

# Generator Limits
for k in range(K):
    for t in range(T):
        for i in range(data['num'][k]):
            problem += (data['minlevel'][k] * numon[k][t] <= pwr[k][t][i])
            problem += (pwr[k][t][i] <= data['maxlevel'][k] * numon[k][t])

# Unit Commitment
for k in range(K):
    for t in range(T):
        problem += (numon[k][t] <= data['num'][k])

# Startup Calculation
for k in range(K):
    for t in range(1, T):  # Start from t=1 to use t-1
        problem += (startup[k][t] >= numon[k][t] - numon[k][t-1])

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')