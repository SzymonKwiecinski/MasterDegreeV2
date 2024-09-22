import pulp
import json

# Input data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'manpower_limit': 470000000.0
}

K = len(data['stock'])
T = 2  # considering two years

# Create the problem variable
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective function
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(T)), "Total Production"

# Constraints
# Manpower constraints
for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= data['manpower_limit']), f"Manpower_Limit_Year_{t}"

# Production and Capacity constraints for Year 1 and Year 2
for k in range(K):
    for t in range(T):
        problem += (produce[k][t] <= data['stock'][k] + (data['capacity'][k] if t > 0 else 0)), f"Production_Capacity_{k}_{t}"

# Input requirements for production
for k in range(K):
    for t in range(T):
        for j in range(K):
            if t > 0:
                problem += (produce[k][t] <= data['inputone'][k][j] * produce[j][t - 1]), f"Input_Requirement_{k}_{t}_{j}"

# Input requirements for building capacity
for k in range(K):
    for t in range(T):
        for j in range(K):
            if t > 0:
                problem += (buildcapa[k][t] <= data['inputtwo'][k][j] * produce[j][t - 1]), f"Build_Input_Requirement_{k}_{t}_{j}"

# Solve the problem
problem.solve()

# Prepare output
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

# Result output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')