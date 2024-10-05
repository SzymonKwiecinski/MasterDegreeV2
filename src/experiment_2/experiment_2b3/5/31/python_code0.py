import pulp

# Load data from JSON
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
T = len(data['demand'])  # Number of periods
K = len(data['num'])  # Number of generator types

# Problem
problem = pulp.LpProblem("Generator_Operation", pulp.LpMinimize)

# Variables
numon = [[pulp.LpVariable(f"numon_{k}_{t}", lowBound=0, upBound=data['num'][k], cat='Integer') for t in range(T)] for k in range(K)]
extra_mw = [[pulp.LpVariable(f"extra_mw_{k}_{t}", lowBound=0, cat='Continuous') for t in range(T)] for k in range(K)]

# Objective function
total_cost = (
    pulp.lpSum(data['runcost'][k] * numon[k][t] +
               data['extracost'][k] * extra_mw[k][t] +
               data['startcost'][k] * pulp.lpSum([numon[k][t] for t in range(T)])
               for k in range(K) for t in range(T))
)

problem += total_cost

# Constraints

# Demand satisfaction
for t in range(T):
    problem += (
        pulp.lpSum(data['minlevel'][k] * numon[k][t] + extra_mw[k][t] for k in range(K)) >= data['demand'][t],
        f"Demand_Constraint_{t}"
    )

# Generator capacity constraints
for k in range(K):
    for t in range(T):
        problem += (
            extra_mw[k][t] <= (data['maxlevel'][k] - data['minlevel'][k]) * numon[k][t],
            f"Capacity_Constraint_{k}_{t}"
        )

# Solve
problem.solve()

# Prepare output
numon_output = [[pulp.value(numon[k][t]) for t in range(T)] for k in range(K)]

# Print results
result = {"numon": numon_output}
print(result)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')