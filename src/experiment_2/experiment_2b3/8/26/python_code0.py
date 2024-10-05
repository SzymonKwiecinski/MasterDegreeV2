import pulp

# Load data
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "demand": [60000000.0, 60000000.0, 30000000.0]
}

# Number of industries
K = len(data['inputone'])
# Planning horizon
T = 5

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function: Maximize the total manpower requirement over five years
problem += pulp.lpSum(
    (data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t])
    for k in range(K) for t in range(T)
)

# Constraints
for k in range(K):
    # Initial stock constraint for year 0
    problem += (stockhold[k, 0] == data['stock'][k] + produce[k, 0] - data['capacity'][k] - buildcapa[k, 0])
    
    for t in range(1, T):
        # Stock balance equation for each year t
        problem += (stockhold[k, t] == stockhold[k, t - 1] + produce[k, t] - data['demand'][k] - buildcapa[k, t])
        
        # Capacity constraint for production
        problem += (produce[k, t] <= data['capacity'][k] + sum(buildcapa[k, t_2] for t_2 in range(max(0, t - 2), t)))
    
    # Demand constraints for years 1 to T
    for t in range(1, T):
        problem += (produce[k, t] + stockhold[k, t - 1] >= data['demand'][k])

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')