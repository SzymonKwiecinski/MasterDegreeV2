import pulp

# Data
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "demand": [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['manpowerone'])  # Number of industries
T = 5  # Number of years

# Problem
problem = pulp.LpProblem("Maximize_Total_Manpower", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Initial stock in year 0
for k in range(K):
    stockhold[k, 0].setInitialValue(data['stock'][k])

# Capacity constraints
for k in range(K):
    problem += produce[(k, 0)] <= data['capacity'][k]

# Demand and stockholding constraints
for t in range(1, T):
    for k in range(K):
        problem += produce[(k, t)] + stockhold[(k, t-1)] == data['demand'][k] + stockhold[(k, t)]
        problem += produce[(k, t)] <= data['capacity'][k]

# Capacity building constraints
for k in range(K):
    for t in range(T-2):  # since capacity building affects from t+2
        problem += buildcapa[(k, t)] * data['manpowertwo'][k] <= (data['capacity'][k] - produce[(k, t)])

# Manpower requirement objective
total_manpower = pulp.lpSum([produce[(k, t)] * data['manpowerone'][k] for k in range(K) for t in range(T)])
problem += total_manpower

# Solve
problem.solve()

# Prepare output format
output = {
    "produce": [[produce[k, t].varValue for t in range(T)] for k in range(K)],
    "buildcapa": [[buildcapa[k, t].varValue for t in range(T)] for k in range(K)],
    "stockhold": [[stockhold[k, t].varValue for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')