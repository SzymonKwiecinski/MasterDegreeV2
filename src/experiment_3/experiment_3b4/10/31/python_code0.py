import pulp

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

# Indices
T = len(data['demand'])
K = len(data['num'])

# Problem
problem = pulp.LpProblem("PowerStationCommitment", pulp.LpMinimize)

# Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)),
                              lowBound=0, cat='Continuous')

output = pulp.LpVariable.dicts("output", ((k, t) for k in range(K) for t in range(T)),
                               lowBound=0, cat='Continuous')

start = pulp.LpVariable.dicts("start", ((k, t) for k in range(K) for t in range(T)),
                              lowBound=0, upBound=1, cat='Binary')

# Objective Function
problem += pulp.lpSum(
    data['runcost'][k] * numon[k, t] +
    data['extracost'][k] * (output[k, t] - data['minlevel'][k] * numon[k, t]) +
    data['startcost'][k] * start[k, t]
    for t in range(T) for k in range(K)
)

# Constraints
# Meet demand
for t in range(T):
    problem += pulp.lpSum(output[k, t] for k in range(K)) >= data['demand'][t], f"Demand_Constraint_{t}"

# Generator output limits
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k, t] <= output[k, t], f"Min_Output_Constraint_{k}_{t}"
        problem += output[k, t] <= data['maxlevel'][k] * numon[k, t], f"Max_Output_Constraint_{k}_{t}"

# Maximum number of generators of type k
for k in range(K):
    for t in range(T):
        problem += numon[k, t] <= data['num'][k], f"Max_Num_On_Constraint_{k}_{t}"

# Start condition
for k in range(K):
    for t in range(1, T):
        problem += start[k, t] >= numon[k, t] - numon[k, t - 1], f"Start_Condition_{k}_{t}"

# Solve the problem
problem.solve()

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')