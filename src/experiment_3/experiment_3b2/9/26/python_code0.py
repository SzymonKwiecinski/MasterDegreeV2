import pulp
import json

# Load data
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

# Define sets and parameters
K = len(data['manpowerone'])  # Number of industries
T = 5  # Number of years

# Create the problem variable
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(1, T+1)), lowBound=0)  # Units produced
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(1, T+1)), lowBound=0)  # Capacity built
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(1, T+1)), lowBound=0)  # Stock held

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] for k in range(K) for t in range(1, T+1))

# Constraints

# Initial stock and capacity constraints
for k in range(K):
    stockhold[k][0] = data['stock'][k]
    # capacity[k][0] = data['capacity'][k]  # Initial capacity is set by default

# Capacity constraints
for k in range(K):
    for t in range(1, T+1):
        problem += produce[k][t] + buildcapa[k][t] <= data['capacity'][k] + pulp.lpSum(buildcapa[k][i] for i in range(1, t)), f"CapacityConstraint_k{str(k)}_t{str(t)}"

# Stock balance constraints
for k in range(K):
    for t in range(1, T+1):
        problem += (stockhold[k][t] == 
                     stockhold[k][t-1] + produce[k][t] - pulp.lpSum(data['inputone'][k][j] * produce[j][t] for j in range(K)) - data['demand'][k], 
                     f"StockBalance_k{str(k)}_t{str(t)}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')