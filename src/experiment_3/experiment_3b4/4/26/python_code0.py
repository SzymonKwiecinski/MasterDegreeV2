import pulp

# Data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['manpowerone'])
T = 5

# Initialize problem
problem = pulp.LpProblem("Manpower_Requirement_Maximization", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K+1) for t in range(1, T+1)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * produce[(k, t)] + data['manpowertwo'][k] * buildcapa[(k, t)]
                      for k in range(K) for t in range(1, T+1))

# Constraints
for t in range(1, T+1):
    for k in range(K):
        # Demand satisfaction
        problem += (produce[(k, t)] + (stockhold[(k, t-1)] if t > 1 else data['stock'][k])
                    - pulp.lpSum(data['inputone'][k][j] * produce[(j, t)] for j in range(K))
                    - data['demand'][k] >= 0)

        # Capacity constraints
        problem += produce[(k, t)] + buildcapa[(k, t)] <= (data['capacity'][k] if t == 1 else stockhold[(k+1, t-1)])
        
        # Resource constraints
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[(j, t)] for j in range(K)) <= produce[(k, t)]

# Initial stocks constraints for year t=0 accounted by not including in loop
for k in range(K):
    stockhold[(k, 0)] = data['stock'][k]

# Capacity Built-in Constraints
for t in range(2, T+1):
    for k in range(K):
        problem += stockhold[(k+1, t-1)] == stockhold[(k+1, t-2)] + buildcapa[(k, t-2)]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')