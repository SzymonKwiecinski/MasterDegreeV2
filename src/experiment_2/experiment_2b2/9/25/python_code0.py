import pulp

# Load data from JSON format
data = {
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "manpower_limit": 470000000.0
}

inputone = data["inputone"]
manpowerone = data["manpowerone"]
inputtwo = data["inputtwo"]
manpowertwo = data["manpowertwo"]
stock = data["stock"]
capacity = data["capacity"]
manpower_limit = data["manpower_limit"]

K = len(inputone)  # Number of industries
T = 4  # Considering 4 years for planning: year 0, 1, 2, 3

# Initialize the problem
problem = pulp.LpProblem("Maximize_Total_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective: Maximize total production in the last two years (year 2 and 3)
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in range(2, 4))

# Constraints

# Initial stockhold equals the initial stock
for k in range(K):
    problem += stockhold[k, 0] == stock[k]

# Capacity constraints for each industry and year
for k in range(K):
    for t in range(T):
        total_output = produce[k, t] + buildcapa[k, t]
        if t == 0:
            problem += total_output <= capacity[k]
        elif t == 1:
            problem += total_output <= capacity[k] + buildcapa[k, 0]
        else:
            problem += total_output <= capacity[k] + buildcapa[k, 0] + buildcapa[k, 1]

# Manpower constraints for each year
for t in range(T):
    problem += pulp.lpSum(produce[k, t] * manpowerone[k] + buildcapa[k, t] * manpowertwo[k] for k in range(K)) <= manpower_limit

# Material balance for each industry and year
for k in range(K):
    for t in range(1, T):
        input_usage = pulp.lpSum(produce[j, t-1] * inputone[k][j] for j in range(K)) + pulp.lpSum(buildcapa[j, max(0, t-2)] * inputtwo[k][j] for j in range(K))
        problem += produce[k, t] + stockhold[k, t] == input_usage + stockhold[k, t-1]

# Solve the problem
problem.solve()

# Collect results
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(1, T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(1, T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(1, T)] for k in range(K)]
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')