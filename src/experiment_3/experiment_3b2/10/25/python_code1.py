import pulp
import json

# Data input
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'manpower_limit': 470000000.0
}

K = len(data['inputone'])
T = 3  # Considering the last 2 years plus year 0

# Define the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("Produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("BuildCapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("StockHold", (range(K), range(T)), lowBound=0)
capacity = pulp.LpVariable.dicts("Capacity", (range(K), range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T-1, T))

# Initial conditions
for k in range(K):
    stockhold[k][0] = data['stock'][k]
    capacity[k][0] = data['capacity'][k]

# Constraints
for t in range(T):
    for k in range(K):
        # Production Constraints
        if t > 0:
            problem += produce[k][t] + buildcapa[k][t] <= capacity[k][t - 1] + stockhold[k][t - 1]

        # Stock Balance
        problem += stockhold[k][t] == stockhold[k][t - 1] + produce[k][t] - \
                   pulp.lpSum(data['inputone'][j][k] * produce[j][t] for j in range(K) if t > 0) - \
                   pulp.lpSum(data['inputtwo'][j][k] * buildcapa[j][t] for j in range(K))

        # Capacity Expansion
        if t >= 2:
            problem += capacity[k][t] == capacity[k][t - 1] + buildcapa[k][t - 2]

    # Manpower Limit
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + 
                           data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= data['manpower_limit']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')