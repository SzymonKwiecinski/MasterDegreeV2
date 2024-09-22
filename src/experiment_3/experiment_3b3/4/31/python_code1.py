import pulp

# Data Input
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
problem = pulp.LpProblem("Generator_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), 
                              lowBound=0, cat=pulp.LpContinuous)  # Fixed here
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), 
                              lowBound=0, cat=pulp.LpContinuous)
startup = pulp.LpVariable.dicts("startup", ((k, t) for k in range(K) for t in range(T)), 
                                cat=pulp.LpBinary)

# Objective Function
problem += pulp.lpSum(data['runcost'][k] * numon[k, t] + 
                      data['extracost'][k] * pulp.lpMax(0, level[k, t] - data['minlevel'][k]) * numon[k, t] +
                      data['startcost'][k] * startup[k, t] 
                      for k in range(K) for t in range(T))

# Constraints
for t in range(T):
    # Demand Constraint
    problem += pulp.lpSum(level[k, t] for k in range(K)) >= data['demand'][t]

for k in range(K):
    for t in range(T):
        # Generation Level Constraints
        problem += data['minlevel'][k] * numon[k, t] <= level[k, t]
        problem += level[k, t] <= data['maxlevel'][k] * numon[k, t]
        
        # On/Off Constraint (redundant as it's included in Generation Level)
        problem += level[k, t] <= data['maxlevel'][k] * numon[k, t]

    # Startup Constraint
    for t in range(1, T):
        problem += startup[k, t] >= numon[k, t] - numon[k, t-1]
    problem += startup[k, 0] == numon[k, 0]

# Solve the problem
problem.solve()

# Output Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output Variables
numon_output = [[pulp.value(numon[k, t]) for t in range(T)] for k in range(K)]
print("Numon:", numon_output)