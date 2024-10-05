import pulp

# Data from JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['manpowerone'])  # Number of industries
T = 1  # Single time period for simplicity
M = 1000000  # Maximum available manpower

# Create a problem
problem = pulp.LpProblem("Industry_Production_Problem", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * produce[(k, t)] + data['manpowertwo'][k] * buildcapa[(k, t)]
                      for k in range(K) for t in range(T))

# Constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += (produce[(k, t)] + data['stock'][k]
                        == pulp.lpSum(data['inputone'][k][j] * (produce[(j, t-1)] if t > 0 else 0)
                                      for j in range(K)) + stockhold[(k, t)] + data['demand'][k])

        problem += (buildcapa[(k, t)]
                    <= data['capacity'][k] + (data['stock'][k] if t == 0 else stockhold[(k, t-1)])
                    + pulp.lpSum(data['inputtwo'][k][j] * (produce[(j, t-1)] if t > 0 else 0) for j in range(K)))

for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[(k, t)] + data['manpowertwo'][k] * buildcapa[(k, t)]
                           for k in range(K)) <= M)

for k in range(K):
    for t in range(T):
        if t == 0:
            problem += (stockhold[(k, t)] == data['stock'][k] + produce[(k, t)] - data['demand'][k])

# Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')