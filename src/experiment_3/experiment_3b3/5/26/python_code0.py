import pulp
import json

# Define the number of industries and years
K = 3
T = 5

# Load data from JSON format
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
demand = data['demand']

# Problem instance
problem = pulp.LpProblem("Manpower_Maximization", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(manpowerone[k] * produce[k, t] + manpowertwo[k] * buildcapa[k, t] for k in range(K) for t in range(T))

# Constraints
for k in range(K):
    for t in range(T):
        # Production constraints
        problem += (produce[k, t] + 
                    (stockhold[k, t-1] if t > 0 else 0) - 
                    stockhold[k, t] ==
                    pulp.lpSum(inputone[k][j] * (produce[j, t-1] if t > 0 else 0) for j in range(K)) +
                    pulp.lpSum(inputtwo[k][j] * (buildcapa[j, t-2] if t > 1 else 0) for j in range(K)) +
                    stock[k])

        # Demand satisfaction
        if t > 0:
            problem += (produce[k, t] + (stockhold[k, t-1] if t > 0 else 0) - stockhold[k, t] >= demand[k])

        # Capacity constraints
        problem += (produce[k, t] + buildcapa[k, t] <= capacity[k])

# Solve problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')