import pulp
import json

# Data from JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

K = len(data['inputone'])  # Number of industries
T = 3  # Number of years to simulate

# Create the problem
problem = pulp.LpProblem("Economic_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function
problem += pulp.lpSum(produce[k, T-1] + produce[k, T] for k in range(K)), "Total_Production"

# Constraints
# Production constraints
for k in range(K):
    for t in range(T):
        problem += produce[k, t] <= data['capacity'][k] + (stockhold[k, t-1] if t > 0 else data['stock'][k]), f"Prod_Constraint_{k}_{t}"

# Input constraints
for k in range(K):
    for t in range(1, T):
        problem += (pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) +
                     pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t-2] for j in range(K))) >= produce[k, t], f"Input_Constraint_{k}_{t}"

# Manpower constraints
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) + \
               pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'], f"Manpower_Constraint_{t}"

# Stock balance constraints
for k in range(K):
    for t in range(1, T):
        problem += stockhold[k, t] == (stockhold[k, t-1] + produce[k, t-1] - \
                                         pulp.lpSum(data['inputone'][j][k] * produce[j, t-1] for j in range(K)) - \
                                         stockhold[k, t-1]), f"Stock_Balance_{k}_{t}"

# Building capacity constraints
for k in range(K):
    for t in range(T - 1):
        problem += pulp.lpSum(buildcapa[j, t-1] for j in range(K)) + data['capacity'][k] == data['capacity'][k] + \
                   pulp.lpSum(buildcapa[j, t-1] for j in range(K)), f"Capacity_Building_{k}_{t}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')