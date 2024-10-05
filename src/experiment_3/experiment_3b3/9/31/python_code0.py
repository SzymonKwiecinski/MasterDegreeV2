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

T = len(data['demand'])
K = len(data['num'])

# Problem
problem = pulp.LpProblem("Electricity_Demand_Management", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
level = pulp.LpVariable.dicts("level", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
start = pulp.LpVariable.dicts("start", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['runcost'][k] * numon[k, t] + 
                      data['extracost'][k] * level[k, t] +
                      data['startcost'][k] * start[k, t] 
                      for k in range(K) for t in range(T))

# Constraints
# Demand Satisfaction
for t in range(T):
    problem += (pulp.lpSum(numon[k, t] * data['minlevel'][k] + level[k, t] for k in range(K)) >= data['demand'][t])

# Generator Capacity
for k in range(K):
    for t in range(T):
        problem += (numon[k, t] * data['minlevel'][k] <= level[k, t])
        problem += (level[k, t] <= numon[k, t] * data['maxlevel'][k])

# Startup Decisions
for k in range(K):
    for t in range(T):
        problem += (start[k, t] <= numon[k, t])

# Availability of Generators
for k in range(K):
    for t in range(T):
        problem += (numon[k, t] <= data['num'][k])

# Solve the problem
problem.solve()

# Output Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')