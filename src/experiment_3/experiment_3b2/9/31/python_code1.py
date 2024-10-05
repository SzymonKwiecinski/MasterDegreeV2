import pulp
import json

# Data in JSON format
data = {'demand': [15000, 30000, 25000, 40000, 27000], 
        'num': [12, 10, 5], 
        'minlevel': [850, 1250, 1500], 
        'maxlevel': [2000, 1750, 4000], 
        'runcost': [1000, 2600, 3000], 
        'extracost': [2.0, 1.3, 3.0], 
        'startcost': [2000, 1000, 500]}

# Parameters
T = len(data['demand'])  # Number of time periods
K = len(data['num'])      # Number of plants

# Problem definition
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Integer')
p = pulp.LpVariable.dicts("p", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(x[k, t] * data['runcost'][k] + p[k, t] * data['extracost'][k] + y[k, t] * data['startcost'][k]
                       for k in range(K) for t in range(T))

# Demand Constraints
for t in range(T):
    problem += pulp.lpSum(x[k, t] * data['minlevel'][k] for k in range(K)) + pulp.lpSum(p[k, t] for k in range(K)) >= data['demand'][t]

# Power Output Constraints
for k in range(K):
    for t in range(T):
        problem += p[k, t] <= (data['maxlevel'][k] - data['minlevel'][k]) * x[k, t]

# Startup Constraint
for k in range(K):
    for t in range(T):
        problem += x[k, t] <= data['num'][k] * y[k, t]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')