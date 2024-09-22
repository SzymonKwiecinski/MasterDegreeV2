import pulp
import json

# Data from the provided JSON
data = json.loads('{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}')

# Parameters
T = len(data['demand'])  # Total number of time periods
K = len(data['num'])      # Total number of generator types

# Create a linear programming problem
problem = pulp.LpProblem("Electricity_Demand_Allocation", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, upBound=None, cat='Integer')
level = pulp.LpVariable.dicts("level", (range(K), range(T)), lowBound=0, upBound=None)
startup = pulp.LpVariable.dicts("startup", (range(K), range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['runcost'][k] * numon[k][t] + 
                       data['extracost'][k] * (level[k][t] - data['minlevel'][k]) * numon[k][t] +
                       data['startcost'][k] * startup[k][t] 
                       for k in range(K) for t in range(T))

# Constraints
# Demand Satisfaction
for t in range(T):
    problem += pulp.lpSum(level[k][t] for k in range(K)) >= data['demand'][t]

# Operational Level Constraints
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k][t] <= level[k][t]
        problem += level[k][t] <= data['maxlevel'][k] * numon[k][t]

# Number of Generators On
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= data['num'][k]

# Startup Indicator
for k in range(K):
    for t in range(1, T):
        problem += startup[k][t] >= numon[k][t] - numon[k][t-1]

# Initial condition for startup at t=1
for k in range(K):
    problem += startup[k][0] == numon[k][0]

# Solve the problem
problem.solve()

# Print the results
for k in range(K):
    for t in range(T):
        print(f'numon[{k},{t}] = {numon[k][t].varValue}')
        
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')