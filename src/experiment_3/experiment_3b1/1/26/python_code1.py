import pulp
import json

# Load data
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

K = len(data['manpowerone'])  # Number of industries
T = 5  # Number of years

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (k for k in range(K)), lowBound=0)

# Create the problem
problem = pulp.LpProblem("Economic_Production", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K) for t in range(1, T + 1))

# Constraints
for k in range(K):
    stockhold[k] = data['stock'][k]
    
for t in range(1, T + 1):
    for k in range(K):
        problem += produce[k, t] <= stockhold[k] + data['capacity'][k]

    for k in range(K):
        problem += stockhold[k] == stockhold[k] + produce[k, t] - data['demand'][k]  # Initial stock added later
        
        # Update stockhold for subsequent years
        if t > 1:
            stockhold[k] = pulp.LpVariable(f'stockhold_{k}_{t-1}', lowBound=0)
    
    for k in range(K):
        problem += pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] + data['inputtwo'][k][j] * buildcapa[j, t-1] for j in range(K)) >= produce[k, t]

# Capacity Building Constraints
for k in range(K):
    problem += data['capacity'][k] >= pulp.lpSum(buildcapa[k, t] for t in range(1, T + 1))

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')