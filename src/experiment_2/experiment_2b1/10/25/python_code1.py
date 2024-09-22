import pulp
import numpy as np
import json

# Data provided in JSON format
data_json = """{
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    "manpowerone": [0.6, 0.3, 0.2], 
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    "manpowertwo": [0.4, 0.2, 0.1], 
    "stock": [150, 80, 100], 
    "capacity": [300, 350, 280], 
    "manpower_limit": 470000000.0
}"""

data = json.loads(data_json)

K = len(data['inputone'])  # Number of industries
T = 3  # Number of years considered (0, 1, 2)

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective Function: Maximize total production in the last two years
problem += pulp.lpSum([produce[k][t] for k in range(K) for t in range(T - 2, T)])

# Constraints
# Manpower constraints for all years
for t in range(T):
    problem += pulp.lpSum([data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)]) <= data['manpower_limit']

# Capacity and input constraints
for k in range(K):
    for t in range(T):
        if t > 0:  # From Year 1 and onwards we need to consider inputs
            problem += pulp.lpSum([data['inputone'][k][j] * produce[j][t - 1] for j in range(K)]) + stockhold[k][t - 1] >= produce[k][t]
            problem += pulp.lpSum([data['inputtwo'][k][j] * buildcapa[j][t - 1] for j in range(K)]) + stockhold[k][t - 1] >= buildcapa[k][t]
        
        # Stock balance constraint
        if t > 0:
            problem += stockhold[k][t] == stockhold[k][t - 1] + produce[k][t] - pulp.lpSum([data['inputone'][k][j] * produce[j][t] for j in range(K)])
        else:
            problem += stockhold[k][t] == data['stock'][k] + produce[k][t]  # Initial stock for year 0

# Initial capacities
for k in range(K):
    for t in range(T):
        problem += produce[k][t] <= data['capacity'][k]  # Limit production by capacity

# Solve the problem
problem.solve()

# Prepare output
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')