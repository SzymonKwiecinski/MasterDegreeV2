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

# Define the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Variables
K = len(data['num'])  # Number of generator types
T = len(data['demand'])  # Number of time periods

# numon[k][t] is the number of generators of type k on during period t
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')

# total_cost to minimize
total_cost = pulp.lpSum(
    (data['runcost'][k] + data['extracost'][k] * (data['demand'][t] - data['minlevel'][k]) * numon[k][t]) + 
    (data['startcost'][k] if numon[k][t] > 0 else 0) 
    for k in range(K) for t in range(T)
)

problem += total_cost

# Constraints
for t in range(T):
    demand_constraint = pulp.lpSum(numon[k][t] * data['maxlevel'][k] for k in range(K)) >= data['demand'][t]
    problem += demand_constraint

    # Minimum level constraint
    for k in range(K):
        problem += numon[k][t] * data['minlevel'][k] <= data['maxlevel'][k] * numon[k][t]

# Solve the problem
problem.solve()

# Output the results
numon_result = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]

output = {
    "numon": numon_result
}

print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')