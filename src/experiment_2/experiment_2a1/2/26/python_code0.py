import pulp
import json

data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['manpowerone'])  # Number of industries
T = 5  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective Function: maximize total manpower requirement over five years
problem += pulp.lpSum(data['manpowerone'][k] * (produce[k, t] + buildcapa[k, t]) for k in range(K) for t in range(T)), "Total_Manpower_Requirement"

# Constraints
for k in range(K):
    for t in range(T):
        # Stock flow constraints
        if t == 0:  # Initial stock is available at year 0
            problem += stockhold[k, t] == data['stock'][k] + produce[k, t], f"Stock_Initial_{k}_{t}"
        else:
            problem += stockhold[k, t] == stockhold[k, t-1] + produce[k, t] - data['demand'][k], f"Stock_Flow_{k}_{t}"

        # Capacity constraints
        if t < T - 1:  # Because we need capacity building to take effect from year t+2
            problem += (produce[k, t] + buildcapa[k, t] <= data['capacity'][k] + pulp.lpSum(buildcapa[k_, t-1] for k_ in range(K)), f"Capacity_Constraint_{k}_{t}")

        # Inputs from other industries
        problem += (pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K) if t > 0) + pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t-2] for j in range(K) if t > 1) <= data['capacity'][k],
                       f"Input_Constraint_{k}_{t}")

# Solve the problem
problem.solve()

# Prepare output
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')