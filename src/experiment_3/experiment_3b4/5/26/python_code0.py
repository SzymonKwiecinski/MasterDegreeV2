import pulp
import json

# Load data
data = json.loads('''{
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "demand": [60000000.0, 60000000.0, 30000000.0]
}''')

K = len(data['manpowerone'])
T = 5  # Number of years

# Initialize the model
problem = pulp.LpProblem("Economic_Planning", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T + 1)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(
    data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t]
    for k in range(K) for t in range(T)
)

# Constraints
for k in range(K):
    # Initial conditions for stockhold and capacity
    stockhold[k, 0] = data['stock'][k]

    # Production and Capacity Constraints
    for t in range(T):
        problem += produce[k, t] + buildcapa[k, t] <= data['capacity'][k]

    # Capacity Update Constraints
    for t in range(2, T):
        problem += data['capacity'][k] == data['capacity'][k] + buildcapa[k, t - 2]

    # Stock Balance Constraints
    for t in range(1, T + 1):
        problem += stockhold[k, t] == stockhold[k, t - 1] + produce[k, t - 1] - pulp.lpSum(data['inputone'][j][k] * produce[j, t - 1] for j in range(K)) - data['demand'][k]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')