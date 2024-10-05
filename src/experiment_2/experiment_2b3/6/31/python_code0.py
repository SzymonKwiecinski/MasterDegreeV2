import pulp

# Data from the provided JSON
data = {
    'demand': [15000, 30000, 25000, 40000, 27000],
    'num': [12, 10, 5],
    'minlevel': [850, 1250, 1500],
    'maxlevel': [2000, 1750, 4000],
    'runcost': [1000, 2600, 3000],
    'extracost': [2.0, 1.3, 3.0],
    'startcost': [2000, 1000, 500]
}

# Extracting data
demand = data['demand']
num = data['num']
minlevel = data['minlevel']
maxlevel = data['maxlevel']
runcost = data['runcost']
extracost = data['extracost']
startcost = data['startcost']

# Time periods and generator types
T = len(demand)
K = len(num)

# Initialize problem
problem = pulp.LpProblem("Generator_Operation_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((k, t) for k in range(K) for t in range(T)), 
                          lowBound=0, cat=pulp.LpContinuous)

y = pulp.LpVariable.dicts("y", ((k, t) for k in range(K) for t in range(T)), 
                          cat=pulp.LpBinary)

z = pulp.LpVariable.dicts("z", ((k, t) for k in range(K) for t in range(T)), 
                          cat=pulp.LpBinary)

# Objective Function
total_cost = pulp.lpSum(
    [y[k, t] * num[k] * runcost[k]
     + x[k, t] * extracost[k]
     + z[k, t] * startcost[k] for k in range(K) for t in range(T)]
)

problem += total_cost

# Constraints
for t in range(T):
    # Demand satisfaction constraint
    problem += pulp.lpSum([x[k, t] for k in range(K)]) >= demand[t]
    
    for k in range(K):
        # Minimum and maximum level constraints
        problem += x[k, t] >= y[k, t] * num[k] * minlevel[k]
        problem += x[k, t] <= y[k, t] * num[k] * maxlevel[k]
        
        # Startup constraint
        if t > 0:
            problem += z[k, t] >= y[k, t] - y[k, t-1]
        else:
            problem += z[k, t] >= y[k, t]

# Solve the problem
problem.solve()

# Extract the solution
numon = [[int(y[k, t].varValue * num[k]) for t in range(T)] for k in range(K)]

output = {
    "numon": numon
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
output