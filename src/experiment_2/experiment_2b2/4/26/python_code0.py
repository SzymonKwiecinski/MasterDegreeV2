import pulp

# Input data
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "demand": [60000000.0, 60000000.0, 30000000.0]
}

# Constants
K = len(data["demand"])  # Number of industries
T = 5  # Planning over 5 years

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)

# Objective function: Maximize the total manpower requirement over five years
problem += pulp.lpSum(
    produce[k, t] * data["manpowerone"][k] + buildcapa[k, t] * data["manpowertwo"][k]
    for k in range(K) for t in range(1, T + 1)
)

# Constraints
for t in range(1, T + 1):
    for k in range(K):
        # Capacity constraints
        if t == 1:
            # Initial capacity and stock
            initial_capacity = data["capacity"][k]
            initial_stock = data["stock"][k]
            problem += (
                produce[k, t] + buildcapa[k, t] <= initial_capacity + initial_stock - stockhold[k, t]
            )
        else:
            # Update capacity considering additional capacity built
            additional_capacity = pulp.lpSum(buildcapa[k, t - 2] for k in range(K) if t > 2)
            problem += (
                produce[k, t] + buildcapa[k, t] <= additional_capacity + stockhold[k, t - 1] - stockhold[k, t]
            )
        
        # Demand constraints (except year 0)
        if t > 1:
            problem += produce[k, t] >= data["demand"][k]

        # Input requirements for production
        problem += (
            produce[k, t] >= pulp.lpSum(data["inputone"][k][j] * produce[j, t] for j in range(K))
        )

# Solve the problem
problem.solve()

# Prepare output
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(1, T + 1)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(1, T + 1)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(1, T + 1)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')