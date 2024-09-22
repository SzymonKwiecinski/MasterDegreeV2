import pulp
import numpy as np

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

K = len(data['capacity'])  # Number of industries
T = 3  # Number of years

# Create problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective Function: Maximize total production in last two years
problem += pulp.lpSum([produce[k][t] for k in range(K) for t in range(T-2, T)])

# Constraints

# Capacity constraints for each industry
for k in range(K):
    for t in range(T):
        if t > 0:
            problem += (stockhold[k][t-1] + produce[k][t-1] + buildcapa[k][t-1] - 
                         data['inputone'][k][k] * produce[k][t] - 
                         data['inputtwo'][k][k] * buildcapa[k][t] >= 0)

# Manpower constraints for producing goods
for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K)) + 
                pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= data['manpower_limit'])

# Initial stocks
for k in range(K):
    problem += stockhold[k][0] == data['stock'][k]

# Capacity usage constraints
for k in range(K):
    for t in range(T):
        problem += (produce[k][t] <= data['capacity'][k] + pulp.lpSum(buildcapa[j][t-1] for j in range(K) if t > 0))

# Solve Problem
problem.solve()

# Prepare output
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')