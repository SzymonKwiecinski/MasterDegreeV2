import pulp

# Input data from JSON
data = {
    "demand": [15000, 30000, 25000, 40000, 27000],
    "num": [12, 10, 5],
    "minlevel": [850, 1250, 1500],
    "maxlevel": [2000, 1750, 4000],
    "runcost": [1000, 2600, 3000],
    "extracost": [2.0, 1.3, 3.0],
    "startcost": [2000, 1000, 500]
}

T = len(data['demand'])  # Number of periods
K = len(data['num'])    # Number of generator types

# Create the problem
problem = pulp.LpProblem("PowerStationScheduling", pulp.LpMinimize)

# Decision variables
numon = [
    [pulp.LpVariable(f"numon_{k}_{t}", lowBound=0, upBound=data['num'][k], cat='Integer')
     for t in range(T)] for k in range(K)
]

power = [
    [pulp.LpVariable(f"power_{k}_{t}", lowBound=0, cat='Continuous')
     for t in range(T)] for k in range(K)
]

# Objective function
startup_cost = pulp.lpSum(data['startcost'][k] * numon[k][t] for k in range(K) for t in range(T))
running_cost = pulp.lpSum(data['runcost'][k] * numon[k][t] for k in range(K) for t in range(T))
extra_cost = pulp.lpSum(data['extracost'][k] * (power[k][t] - numon[k][t] * data['minlevel'][k])
                        for k in range(K) for t in range(T))
problem += startup_cost + running_cost + extra_cost

# Constraints
for t in range(T):
    # Meet demand
    problem += pulp.lpSum(power[k][t] for k in range(K)) >= data['demand'][t]

    # Generator limits
    for k in range(K):
        problem += power[k][t] >= numon[k][t] * data['minlevel'][k]
        problem += power[k][t] <= numon[k][t] * data['maxlevel'][k]

# Solve the problem
problem.solve()

# Output
numon_output = [[int(pulp.value(numon[k][t])) for t in range(T)] for k in range(K)]
output = {"numon": numon_output}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')