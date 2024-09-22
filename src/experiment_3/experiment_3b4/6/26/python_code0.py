import pulp

# Data from JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['manpowerone'])
T = 5

# Define the Linear Programming problem
problem = pulp.LpProblem("Maximize_Manpower_Utility", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function
problem += pulp.lpSum(
    data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t]
    for k in range(K) for t in range(T)
)

# Constraints
for t in range(T):
    for k in range(K):
        # Initial constraints
        if t == 0:
            problem += produce[k, t] == 0
            problem += stockhold[k, t] == data['stock'][k]
            problem += buildcapa[k, t] <= data['capacity'][k]
        else:
            # Stockholding constraint
            problem += produce[k, t] + stockhold[k, t - 1] >= (data['demand'][k] +
                                                               pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)) +
                                                               pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)))
            # Production capacity
            problem += produce[k, t] <= (data['capacity'][k] + buildcapa[k, t - 2] if t >= 2 else data['capacity'][k])
            # Stockholding update
            problem += stockhold[k, t] == (produce[k, t] + stockhold[k, t - 1] - data['demand'][k] -
                                           pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)) -
                                           pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)))

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')