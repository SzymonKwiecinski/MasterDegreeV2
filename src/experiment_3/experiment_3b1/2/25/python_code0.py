import pulp

# Data from the provided JSON
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
T = 2  # Planning horizon (planning for 2 years)

# Create the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", (range(K), range(T)), lowBound=0)

# Objective function
problem += pulp.lpSum([produce[k][T-1] + produce[k][T] for k in range(K)])

# Constraints
# 1. produce_{k,t} + stock_{k,t-1} <= capacity_k + stock_{k,t}
for k in range(K):
    for t in range(1, T):
        problem += produce[k][t] + stock[k][t-1] <= data['capacity'][k] + stock[k][t]

# 2. Input constraints
for k in range(K):
    for t in range(1, T):
        problem += (
            pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) +
            pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t-1] for j in range(K)) +
            stock[k][t-1] >= produce[k][t]
        )

# 3. Manpower constraints
for t in range(T):
    problem += (
        pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K)) +
        pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= data['manpower_limit']
    )

# 4. Initial stock condition
for k in range(K):
    problem += stock[k][0] == data['stock'][k]

# 5. Build capacity (this is implied in the model as capacity increases)
# Not explicitly coded since it's an implication on production planning

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')