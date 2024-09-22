import pulp
import json

# Input data
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Constants
T = len(data['demand'])  # number of time periods
K = len(data['num'])      # number of generator types

# Problem definition
problem = pulp.LpProblem("Power_Generation_Optimization", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, upBound=data['num'][k], cat='Integer')
power_generated = pulp.LpVariable.dicts("power_generated", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function
problem += pulp.lpSum(
    (data['startcost'][k] * (numon[k, t] > 0) + 
     data['runcost'][k] + 
     data['extracost'][k] * (power_generated[k, t] - data['minlevel'][k] * numon[k, t])) 
    for k in range(K) for t in range(T)
)

# Constraints
for t in range(T):
    # Demand constraint
    problem += pulp.lpSum(power_generated[k, t] for k in range(K)) >= data['demand'][t]

    for k in range(K):
        # Power generation limits
        problem += power_generated[k, t] >= data['minlevel'][k] * numon[k, t]
        problem += power_generated[k, t] <= data['maxlevel'][k] * numon[k, t]

# Solve the problem
problem.solve()

# Result extraction
numon_result = [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]

# Output format
output = {
    "numon": numon_result
}

# Print results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')