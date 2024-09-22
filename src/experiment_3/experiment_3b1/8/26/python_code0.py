import pulp
import json

# Data provided in JSON format
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
Total_Manpower_Available = 100  # Example value for total manpower available

# Initialize problem
problem = pulp.LpProblem("Economy_Optimization", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] 
                      for k in range(K) for t in range(T)), "Total_Manpower_Requirement"

# Constraints
for k in range(K):
    for t in range(T):
        # Production and Capacity Constraints
        if t == 0:
            problem += produce[k][t] + data['stock'][k] == stockhold[k][t] + data['demand'][k]
        else:
            problem += produce[k][t] + stockhold[k][t-1] == stockhold[k][t] + data['demand'][k]
        
        problem += data['capacity'][k] + pulp.lpSum(buildcapa[k][tx] for tx in range(T)) >= (produce[k][t] +
                    pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)))

        # Manpower Constraints
        problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] 
                              for k in range(K)) <= Total_Manpower_Available

# Stock Constraints
for k in range(K):
    for t in range(T):
        problem += stockhold[k][t] >= 0

# Build Capacity Constraints
for k in range(K):
    for t in range(T):
        problem += buildcapa[k][t] >= 0

# Production Non-Negativity Constraints
for k in range(K):
    for t in range(T):
        problem += produce[k][t] >= 0

# Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')