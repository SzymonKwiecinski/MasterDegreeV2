import pulp
import json

# Data Initialization
data = json.loads('{"demand": [15000, 30000, 25000, 40000, 27000], "num": [12, 10, 5], "minlevel": [850, 1250, 1500], "maxlevel": [2000, 1750, 4000], "runcost": [1000, 2600, 3000], "extracost": [2.0, 1.3, 3.0], "startcost": [2000, 1000, 500]}')

T = len(data['demand'])
K = len(data['num'])

# Create the Problem
problem = pulp.LpProblem("Electricity_Generation", pulp.LpMinimize)

# Decision Variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, cat='Integer')
level = pulp.LpVariable.dicts("level", (range(K), range(T)), lowBound=0, cat='Continuous')
startup = pulp.LpVariable.dicts("startup", (range(K), range(T)), cat='Binary')

# Objective Function
problem += pulp.lpSum(data['startcost'][k] * startup[k][t] +
                       data['runcost'][k] * numon[k][t] +
                       data['extracost'][k] * (level[k][t] - data['minlevel'][k]) * numon[k][t]
                       for k in range(K) for t in range(T) if numon[k][t] > 0), "Total Cost"

# Constraints
# Demand Constraint
for t in range(T):
    problem += pulp.lpSum(level[k][t] for k in range(K)) == data['demand'][t], f"Demand_Constraint_{t}"

# Operational Level Constraints
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k][t] <= level[k][t], f"Min_Level_Constraint_{k}_{t}"
        problem += level[k][t] <= data['maxlevel'][k] * numon[k][t], f"Max_Level_Constraint_{k}_{t}"

# Availability of Generators
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= data['num'][k], f"Availability_Constraint_{k}_{t}"

# Startup Binary Constraints
for k in range(K):
    for t in range(T):
        problem += startup[k][t] <= numon[k][t], f"Startup_Binary_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')