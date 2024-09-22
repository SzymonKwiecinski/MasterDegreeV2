import pulp

# Extract data from the provided JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

# Parameters
K = len(data['capacity'])
T = 5  # Horizon length defined as 5 years

# Define LP Problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts(
    "produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous'
)
buildcapa = pulp.LpVariable.dicts(
    "buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous'
)
stockhold = pulp.LpVariable.dicts(
    "stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous'
)

# Objective: Maximize total production in the last two years
problem += pulp.lpSum([produce[k, t] for k in range(K) for t in range(T-2, T)])

# Constraints

# Initial stock and capacity
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k]
    problem += produce[k, 0] <= data['capacity'][k]

# Stock, capacity, and manpower constraints in subsequent years
for t in range(T):
    for k in range(K):
        # Update stock after production and building capacity
        if t > 0:
            problem += stockhold[k, t] == (
                stockhold[k, t-1] - pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K))
                - pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t-2] for j in range(K) if t-2 >= 0)
                + produce[k, t] + buildcapa[k, t]
            )

        if t > 0:
            # Capacity constraint
            problem += produce[k, t] <= (data['capacity'][k] + pulp.lpSum(buildcapa[k, t-n] for n in range(2, t+1)))

        # Manpower constraint
        problem += (
            pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) +
            pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K))
        ) <= data['manpower_limit']

# Solve problem
problem.solve()

# Prepare results
result = {
    "produce": [[produce[k, t].varValue for t in range(T)] for k in range(K)],
    "buildcapa": [[buildcapa[k, t].varValue for t in range(T)] for k in range(K)],
    "stockhold": [[stockhold[k, t].varValue for t in range(T)] for k in range(K)]
}

# Print the results
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')