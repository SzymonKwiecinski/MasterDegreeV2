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

# Constants
K = 3  # number of industries
T = 5  # number of time periods

# Indices
industries = range(K)
time_periods = range(T)

# Initialize the problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in industries for t in time_periods), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in industries for t in time_periods), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in industries for t in (-1,) + tuple(time_periods)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in industries for t in time_periods)

# Constraints
# Initial stock constraints
for k in industries:
    problem += stockhold[k, -1] == data['stock'][k]

# Production and stock balance constraints
for k in industries:
    for t in time_periods:
        if t > 0:  # Ensure t-1 is valid
            problem += (
                produce[k, t] + stockhold[k, t-1] ==
                pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in industries) + stockhold[k, t] + buildcapa[k, t]
            )

# Capacity constraint
for k in industries:
    for t in time_periods:
        problem += (
            produce[k, t] + stockhold[k, t] <= data['capacity'][k] + pulp.lpSum(buildcapa[k, t_prime] for t_prime in range(max(0, t-2)))
        )

# Demand satisfaction constraint
for k in industries:
    for t in time_periods:
        if t > 0:  # Ensure t-1 is valid
            problem += produce[k, t] + stockhold[k, t-1] >= data['demand'][k]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')