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

# Problem initialization
T = len(data['demand'])  # number of periods
K = len(data['num'])    # number of generator types

# Define the problem
problem = pulp.LpProblem("Electricity_Generation", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, upBound=[data['num'][k] for k in range(K)], cat='Integer')
power_generated = pulp.LpVariable.dicts("power_generated", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective function
total_cost = pulp.lpSum([
    (data['runcost'][k] + data['extracost'][k] * (power_generated[k][t] - data['minlevel'][k])) * numon[k][t] + data['startcost'][k] * (numon[k][t] > 0)
    for k in range(K) for t in range(T)
])
problem += total_cost

# Constraints
for t in range(T):
    # Demand constraints
    problem += pulp.lpSum([power_generated[k][t] for k in range(K)]) >= data['demand'][t]

    # Power generation constraints
    for k in range(K):
        # Minimum and maximum generation constraints
        problem += power_generated[k][t] >= data['minlevel'][k] * numon[k][t]
        problem += power_generated[k][t] <= data['maxlevel'][k] * numon[k][t]

    # Total units constraint
    problem += numon[k][t] <= data['num'][k]

# Solve the problem
problem.solve()

# Prepare the output
numon_output = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output format
output = {
    "numon": numon_output
}