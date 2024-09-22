import pulp
import json

# Input data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

# Problem parameters
K = len(data['inputone'])  # Number of industries
T = 5  # Number of years

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), 0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), 0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), 0)

# Objective function: Maximize the total manpower requirement over five years
problem += pulp.lpSum(data['manpowerone'][k] * (produce[k][t] + buildcapa[k][t] for k in range(K) for t in range(T))), "Total_Manpower_Requirement"

# Constraints
for t in range(T):
    for k in range(K):
        # Production must meet demand (except year 0)
        if t > 0:
            problem += (produce[k][t] + stockhold[k][t-1] - stockhold[k][t] >= data['demand'][k]), f"Demand_Constraint_{k}_{t}"

        # Capacity constraint for production
        problem += (produce[k][t] <= data['capacity'][k] + stockhold[k][t]), f"Capacity_Constraint_{k}_{t}"

        # Input requirements for production
        problem += (produce[k][t] <= pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) + stockhold[k][t-1]), f"Input_Requirements_{k}_{t}"

for t in range(1, T):
    for k in range(K):
        # Input requirements for productive capacity
        problem += (buildcapa[k][t] <= pulp.lpSum(data['inputtwo'][k][j] * produce[j][t-2] for j in range(K)) + stockhold[k][t-1]), f"Build_Capa_Requirements_{k}_{t}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')