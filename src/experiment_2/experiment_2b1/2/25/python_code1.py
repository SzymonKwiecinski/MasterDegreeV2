import pulp
import json

# Given data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'manpower_limit': 470000000.0
}

K = len(data['manpowerone'])
T = 2  # The number of years we are interested in

# Create the LP problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function
problem += pulp.lpSum(produce[(k, T-1)] for k in range(K)) + pulp.lpSum(produce[(k, T-2)] for k in range(K))

# Constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += stockhold[(k, t)] == data['stock'][k] + produce[(k, t)] - pulp.lpSum(data['inputone'][k][j] * produce[(j, t)] for j in range(K)), f"Stock_balance_initial_{k}_{t}"
        else:
            problem += stockhold[(k, t)] == stockhold[(k, t-1)] + produce[(k, t)] - pulp.lpSum(data['inputone'][k][j] * produce[(j, t-1)] for j in range(K)), f"Stock_balance_{k}_{t}"

for k in range(K):
    for t in range(T):
        problem += pulp.lpSum(data['inputone'][k][j] * produce[(j, t)] for j in range(K)) + pulp.lpSum(data['inputtwo'][k][j] * buildcapa[(j, t)] for j in range(K)) <= data['capacity'][k], f"Capacity_limit_{k}_{t}"

for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[(k, t)] for k in range(K)) + pulp.lpSum(data['manpowertwo'][k] * buildcapa[(k, t)] for k in range(K)) <= data['manpower_limit'], f"Manpower_limit_{t}"

# Solve the problem
problem.solve()

# Output the results
produce_result = [[pulp.value(produce[(k, t)]) for t in range(T)] for k in range(K)]
buildcapa_result = [[pulp.value(buildcapa[(k, t)]) for t in range(T)] for k in range(K)]
stockhold_result = [[pulp.value(stockhold[(k, t)]) for t in range(T)] for k in range(K)]

output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')