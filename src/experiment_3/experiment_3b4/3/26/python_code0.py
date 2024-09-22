import pulp

# Data input
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

# Define the problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0, cat='Continuous')
capacity = pulp.LpVariable.dicts("capacity", ((k, t) for k in range(K) for t in range(T+2)), lowBound=0, cat='Continuous')

# Initialize stock and capacity for t=0
for k in range(K):
    stock[k, 0] = data['stock'][k]
    capacity[k, 0] = data['capacity'][k]

# Objective function
problem += pulp.lpSum(
    data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t]
    for k in range(K) for t in range(T)
)

# Constraints
for k in range(K):
    for t in range(T):
        # Input requirement for production
        problem += pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)) + data['manpowerone'][k] * produce[k, t] <= capacity[k, t]

        # Input requirement for capacity building
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)) + data['manpowertwo'][k] * buildcapa[k, t] <= stock[k, t]

        # Stock balance
        problem += stock[k, t+1] == stock[k, t] + produce[k, t] - pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)) - data['demand'][k] - buildcapa[k, t]

        # Capacity update
        if t + 2 < T + 2:
            problem += capacity[k, t+2] == capacity[k, t+1] + buildcapa[k, t]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')