import pulp
import json

data = {'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
        'manpowerone': [0.6, 0.3, 0.2], 
        'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
        'manpowertwo': [0.4, 0.2, 0.1], 
        'stock': [150, 80, 100], 
        'capacity': [300, 350, 280], 
        'manpower_limit': 470000000.0}

K = len(data['inputone'])  # number of industries
T = 3  # number of years to consider (0, 1, 2)

# Create the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective Function: Maximize total production in the last two years
problem += pulp.lpSum(produce[(k, t)] for k in range(K) for t in range(T-1, T)) 

# Constraints
# Capacity constraints for production
for k in range(K):
    for t in range(T):
        problem += produce[(k, t)] + stockhold[(k, t)] <= data['capacity'][k] + stockhold[(k, t-1)] if t > 0 else data['stock'][k]

# Requirement constraints for inputs from other industries
for k in range(K):
    for t in range(T):
        if t > 0:
            problem += pulp.lpSum(data['inputone'][k][j] * produce[(j, t-1)] for j in range(K)) >= produce[(k, t)]
        
# Manpower constraints for production
for k in range(K):
    for t in range(T):
        problem += pulp.lpSum(data['manpowerone'][k] * produce[(k, t)]) <= data['manpower_limit']

# Constraints for building capacity
for k in range(K):
    for t in range(T):
        if t < T-1:  # Building capacity can only happen in the first two years
            problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[(j, t)] for j in range(K)) + stockhold[(k, t)] >= buildcapa[(k, t)]
            problem += pulp.lpSum(data['manpowertwo'][k] * buildcapa[(k, t)]) <= data['manpower_limit']

# Solve the problem
problem.solve()

# Output the results
results = {
    "produce": [[pulp.value(produce[(k, t)]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[(k, t)]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[(k, t)]) for t in range(T)] for k in range(K)]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')