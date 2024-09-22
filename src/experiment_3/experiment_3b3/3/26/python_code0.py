import pulp

# Data setup
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = 3  # Number of industries
T = 5  # Time periods

# Define the problem
problem = pulp.LpProblem("Maximize_Manpower_Utilization", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')

# Objective Function
problem += (
    sum(data['manpowerone'][k] * produce[k, t] for k in range(K) for t in range(1, T+1)) +
    sum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K) for t in range(1, T+1))
)

# Constraints
for k in range(K):
    # Production Capacity Constraints
    problem += (
        data['stock'][k] + sum(produce[k, t] for t in range(1, T+1)) + sum(stockhold[k, t-1] if t > 1 else 0 for t in range(1, T+1)) >= data['demand'][k]
    )
    for t in range(1, T+1):
        problem += produce[k, t] <= data['capacity'][k]

        if t > 1:
            # Input Constraints
            problem += (
                sum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) +
                sum(data['inputtwo'][k][j] * buildcapa[j, t-2] if t > 2 else 0 for j in range(K))
                <= stockhold[k, t-1]
            )

        # Manpower Constraints
        problem += (
            data['manpowerone'][k] * produce[k, t] +
            data['manpowertwo'][k] * buildcapa[k, t] <= 1000  # Assuming a total manpower constraint of 1000 as an example
        )

        # Stock Management Constraints
        if t == 1:
            problem += stockhold[k, t] == data['stock'][k] + produce[k, t] - data['demand'][k]
        else:
            problem += stockhold[k, t] == stockhold[k, t-1] + produce[k, t] - data['demand'][k]

# Solve the problem
problem.solve()

# Display the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')