import pulp
import json

# Load data
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "manpower_limit": 470000000.0}')

# Parameters
K = len(data['inputone'])  # Number of industries
T = 2  # Number of time periods (assumed from the context)

# Decision Variables
produce = pulp.LpVariable.dicts('produce', (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts('buildcapa', (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts('stockhold', (range(K), range(T)), lowBound=0, cat='Continuous')

# Create the problem
problem = pulp.LpProblem("Economic_Production", pulp.LpMaximize)

# Objective Function
problem += pulp.lpSum([produce[k][T-1] + produce[k][T] for k in range(K)])

# Constraints
# Initial stock constraints
for k in range(K):
    problem += stockhold[k][0] == data['stock'][k]

# Production constraints
for t in range(1, T):
    for k in range(K):
        problem += produce[k][t] <= data['capacity'][k] + stockhold[k][t-1]

# Input constraints
for t in range(1, T):
    for k in range(K):
        problem += pulp.lpSum([data['inputone'][k][j] * produce[j][t-1] for j in range(K)]) + \
                   pulp.lpSum([data['inputtwo'][k][j] * buildcapa[j][t-2] for j in range(K)]) <= data['capacity'][k]

# Manpower constraints
for t in range(1, T):
    problem += pulp.lpSum([data['manpowerone'][k] * produce[k][t] for k in range(K)]) + \
               pulp.lpSum([data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)]) <= data['manpower_limit']

# Stock balance constraints
for t in range(1, T):
    for k in range(K):
        problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t-1] - \
                   pulp.lpSum([data['inputone'][k][j] * produce[j][t-1] for j in range(K)])

# Capacity building constraints
for k in range(K):
    problem += data['capacity'][k] == pulp.lpSum([buildcapa[k][t] for t in range(1, T)]) + data['capacity'][k]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')