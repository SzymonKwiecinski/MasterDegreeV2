import pulp

# Data from JSON format
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "demand": [60000000.0, 60000000.0, 30000000.0]
}

# Extracting values from data for convenience
inputone = data["inputone"]
manpowerone = data["manpowerone"]
inputtwo = data["inputtwo"]
manpowertwo = data["manpowertwo"]
stock = data["stock"]
capacity = data["capacity"]
demand = data["demand"]

K = len(inputone) # Number of industries
T = 5 # Number of years

# Create LP problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat="Continuous")
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat="Continuous")
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat="Continuous")

# Objective function: Maximize total manpower over 5 years
problem += pulp.lpSum(
    manpowerone[k] * produce[k, t] + manpowertwo[k] * buildcapa[k, t]
    for k in range(K) for t in range(T)
)

# Constraints

# Stock and capacity constraints for the first year
for k in range(K):
    problem += produce[k, 0] <= capacity[k]
    problem += stockhold[k, 0] == stock[k] + produce[k, 0] - buildcapa[k, 0]
    problem += stockhold[k, 0] <= stock[k]

# Capacity and production constraints for subsequent years
for t in range(1, T):
    for k in range(K):
        # Production cannot exceed capacity
        problem += produce[k, t] <= \
                   capacity[k] + pulp.lpSum(buildcapa[k, t - 2] for t - 2 in range(max(0, t - 2), t))
        # Stock flow balance
        problem += stockhold[k, t] == stockhold[k, t - 1] + produce[k, t] - demand[k] - buildcapa[k, t]

# Ensure non-negative stock holdings
for k in range(K):
    for t in range(T):
        problem += stockhold[k, t] >= 0

# Solve the problem
problem.solve()

# Output results
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')