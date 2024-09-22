import pulp
import json

# Load data from JSON format
data_json = '''{"demand": [15000, 30000, 25000, 40000, 27000], 
                "num": [12, 10, 5], 
                "minlevel": [850, 1250, 1500], 
                "maxlevel": [2000, 1750, 4000], 
                "runcost": [1000, 2600, 3000], 
                "extracost": [2.0, 1.3, 3.0], 
                "startcost": [2000, 1000, 500]}'''
data = json.loads(data_json)

# Parameters
T = len(data['demand'])  # Number of periods
K = len(data['num'])      # Number of generator types

# Initialize the problem
problem = pulp.LpProblem("Power_Generation_Cost_Minimization", pulp.LpMinimize)

# Decision variables
numon = pulp.LpVariable.dicts("numon", (range(K), range(T)), lowBound=0, upBound=None, cat='Integer')
level = pulp.LpVariable.dicts("level", (range(K), range(T)), lowBound=0, upBound=None, cat='Continuous')
start = pulp.LpVariable.dicts("start", (range(K), range(T)), cat='Binary')

# Objective function
problem += pulp.lpSum(data['runcost'][k] * numon[k][t] + 
                       data['startcost'][k] * start[k][t] + 
                       0.5 * data['extracost'][k] * (level[k][t] - data['minlevel'][k]) 
                       for k in range(K) for t in range(T))

# Constraints

# Load balance for each time period
for t in range(T):
    problem += pulp.lpSum(level[k][t] for k in range(K)) == data['demand'][t]

# Operational limits for each generator type
for k in range(K):
    for t in range(T):
        problem += data['minlevel'][k] * numon[k][t] <= level[k][t]
        problem += level[k][t] <= data['maxlevel'][k] * numon[k][t]
        
# Number of units operational
for k in range(K):
    for t in range(T):
        problem += numon[k][t] <= data['num'][k]

# Linking level and number of operational units
for k in range(K):
    for t in range(T):
        problem += level[k][t] <= data['maxlevel'][k] * numon[k][t]

# Startup condition
for k in range(K):
    for t in range(T):
        problem += start[k][t] <= numon[k][t]

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')