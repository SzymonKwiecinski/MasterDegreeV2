from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpInteger, value

# Data
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

T = len(data['demand'])
K = len(data['num'])

# Problem
problem = LpProblem("Power_Station_Commitment", LpMinimize)

# Variables
numon = [[LpVariable(f'numon_{k}_{t}', lowBound=0, upBound=data['num'][k], cat=LpInteger) for t in range(T)] for k in range(K)]
power = [[LpVariable(f'power_{k}_{t}', lowBound=data['minlevel'][k] * numon[k][t], upBound=data['maxlevel'][k] * numon[k][t]) for t in range(T)] for k in range(K)]
start = [[LpVariable(f'start_{k}_{t}', cat=LpInteger, lowBound=0, upBound=1) for t in range(T)] for k in range(K)]

# Constraints
for t in range(T):
    problem += lpSum(power[k][t] for k in range(K)) >= data['demand'][t]
    for k in range(K):
        if t == 0:
            problem += start[k][t] >= numon[k][t]
        else:
            problem += start[k][t] >= numon[k][t] - numon[k][t - 1]

# Objective
total_cost = lpSum(
    lpSum(
        data['runcost'][k] * numon[k][t] +
        data['extracost'][k] * (power[k][t] - data['minlevel'][k] * numon[k][t]) +
        data['startcost'][k] * start[k][t]
        for k in range(K)
    )
    for t in range(T)
)

problem += total_cost

# Solve
problem.solve()

# Output
numon_result = [[int(numon[k][t].varValue) for t in range(T)] for k in range(K)]

output = {"numon": numon_result}
print(output)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')