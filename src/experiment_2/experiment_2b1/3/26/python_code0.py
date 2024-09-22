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

K = len(data['inputone'])
T = 5

# Create the problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective function
total_manpower = pulp.lpSum(data['manpowerone'][k] * pulp.lpSum(produce[k, t] for t in range(T)) for k in range(K)) + \
                       pulp.lpSum(data['manpowertwo'][k] * pulp.lpSum(buildcapa[k, t] for t in range(T)) for k in range(K))

problem += total_manpower

# Constraints for each year
for t in range(T):
    for k in range(K):
        # Demand constraints
        if t > 0:  # No demand in year 0
            problem += produce[k, t] + stockhold[k, t-1] - stockhold[k, t] >= data['demand'][k], f"demand_{k}_{t}"
        else:
            problem += stockhold[k, t] == data['stock'][k] + produce[k, t], f"initial_stock_{k}"

        # Capacity constraints
        if t > 0:  # Productions in year t can use capacity built in year t-2
            problem += produce[k, t] <= data['capacity'][k] + pulp.lpSum(buildcapa[k, t-2]), f"capacity_{k}_{t}"

        # Input requirements
        input_eq = pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) + stockhold[k, t] - produce[k, t]
        problem += input_eq >= 0, f"input_req_{k}_{t}"

        # Build capacity requirements
        if t < T-1:  # Can only build capacity if not at the last year
            problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)) + stockhold[k, t] - buildcapa[k, t] >= 0, f"build_capacity_req_{k}_{t}"

# Solve the problem
problem.solve()

# Output results
produce_result = [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)]
buildcapa_result = [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)]
stockhold_result = [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]

output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

# Print the output and the objective value
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')