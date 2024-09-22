import pulp
import json

# Load data from JSON format
data = json.loads('{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}')

# Define parameters
T = len(data['demand'])            # Number of time periods
K = len(data['num'])                # Number of types of generating units

# Create the problem
problem = pulp.LpProblem("Power_Generation_Optimization", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')
power = pulp.LpVariable.dicts("power", (range(K), range(T)), lowBound=0, cat='Continuous')
startup = pulp.LpVariable.dicts("startup", (range(K), range(T)), cat='Binary')

# Objective function
problem += pulp.lpSum(data['runcost'][k] * numon[k][t] +
                      data['extracost'][k] * (power[k][t] - data['minlevel'][k]) * numon[k][t] +
                      data['startcost'][k] * startup[k][t]
                      for k in range(K) for t in range(T))

# Constraints
# Demand satisfaction
for t in range(T):
    problem += pulp.lpSum(power[k][t] for k in range(K)) >= data['demand'][t]

# Power output limits for each generator type
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k][t] <= power[k][t]
        problem += power[k][t] <= data['maxlevel'][k] * numon[k][t]

# Binary startup variable
for k in range(K):
    for t in range(T):
        problem += power[k][t] <= data['maxlevel'][k] * startup[k][t]

# Number of units on limits
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= data['num'][k]

# Solve the problem
problem.solve()

# Output the number of generators on
numon_output = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]

print(f'Number of Generators On: {numon_output}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')