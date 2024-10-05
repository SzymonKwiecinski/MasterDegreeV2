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

# Indices
K = len(data['capacity'])  # Number of products
T = 2  # Time periods T and T-1

# Create LP Problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", [(k, t) for k in range(K) for t in range(T)], lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", [(k, t) for k in range(K) for t in range(T)], lowBound=0)
stock = pulp.LpVariable.dicts("stock", [(k, t) for k in range(K) for t in range(T)], lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in range(T))

# Constraints

# Input Requirement
for k in range(K):
    for t in range(T):
        problem += (
            pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)) +
            pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)) <=
            data['capacity'][k]
        )

# Manpower Limit
for t in range(T):
    problem += (
        pulp.lpSum(
            data['manpowerone'][k] * produce[k, t] + 
            data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)
        ) <= data['manpower_limit']
    )

# Stock Flow
for k in range(K):
    for t in range(1, T):
        problem += (
            stock[k, t] ==
            stock[k, t-1] + produce[k, t-1] -
            pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)) -
            pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K))
        )

# Capacity Update
# It's given for future period, no direct implementation for this period requirement

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')