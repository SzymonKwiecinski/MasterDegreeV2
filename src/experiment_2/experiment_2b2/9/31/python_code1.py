import pulp

# Data from JSON
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
T = len(data['demand'])
K = len(data['num'])

# Problem
problem = pulp.LpProblem("Power_Station_Scheduling", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Integer')
power_above_min = pulp.LpVariable.dicts("power_above_min", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
start_indicator = pulp.LpVariable.dicts("start_indicator", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective Function
total_cost = pulp.lpSum(
    data['runcost'][k] * numon[k, t] +
    data['extracost'][k] * power_above_min[k, t] +
    data['startcost'][k] * start_indicator[k, t]
    for k in range(K) for t in range(T)
)
problem += total_cost

# Constraints
for t in range(T):
    problem += pulp.lpSum(
        numon[k, t] * data['minlevel'][k] + power_above_min[k, t]
        for k in range(K)
    ) >= data['demand'][t]

    for k in range(K):
        # Capacity Constraints
        problem += numon[k, t] <= data['num'][k]
        problem += power_above_min[k, t] <= (data['maxlevel'][k] - data['minlevel'][k]) * numon[k, t]

        # Startup Constraints
        if t == 0:
            problem += start_indicator[k, t] >= numon[k, t] / float(data['num'][k])
        else:
            problem += start_indicator[k, t] >= (numon[k, t] - numon[k, t-1]) / float(data['num'][k])

# Solve the Problem
problem.solve()

# Extract Results
numon_result = [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]

# Output
output = {
    "numon": numon_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')