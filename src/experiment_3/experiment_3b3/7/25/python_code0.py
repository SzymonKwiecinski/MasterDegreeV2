import pulp

# Data from JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

# Constants
K = 3  # Total number of industries
T = 4  # Total number of years

# Initialize the problem
problem = pulp.LpProblem("Economic_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(produce[k, T-1] + produce[k, T-2] for k in range(K))

# Constraints
# Initial conditions
for k in range(K):
    stock[k, 0] = data['stock'][k]

# Production Constraints
for k in range(K):
    for t in range(T):
        problem += produce[k, t] <= stock[k, t-1] + data['capacity'][k]

# Input and Production Requirements
for k in range(K):
    for t in range(T):
        problem += produce[k, t] == pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) + stock[k, t-1]

# Capacity Building Requirements
for k in range(K):
    for t in range(T):
        problem += buildcapa[k, t] <= pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)) + stock[k, t-1]

# Manpower Constraints
for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) +
                pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'])

# Stock Update Rule
for k in range(K):
    for t in range(1, T):
        problem += stock[k, t] == (stock[k, t-1] +
                                   produce[k, t-1] -
                                   pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) -
                                   buildcapa[k, t-1])

# Capacity Increase After Two Years
for k in range(K):
    for t in range(1, T):
        data['capacity'][k] += pulp.lpSum(buildcapa[j, t-1] for j in range(K))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')