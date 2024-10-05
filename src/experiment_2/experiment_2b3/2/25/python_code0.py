import pulp

# Data from the JSON input
data = {'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
        'manpowerone': [0.6, 0.3, 0.2], 
        'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
        'manpowertwo': [0.4, 0.2, 0.1], 
        'stock': [150, 80, 100], 
        'capacity': [300, 350, 280], 
        'manpower_limit': 470000000.0}

inputone = data["inputone"]
manpowerone = data["manpowerone"]
inputtwo = data["inputtwo"]
manpowertwo = data["manpowertwo"]
stock = data["stock"]
capacity = data["capacity"]
manpower_limit = data["manpower_limit"]

K = len(capacity)
T = 4

# Create the LP problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = [[pulp.LpVariable(f"produce_{k}_{t}", lowBound=0) for t in range(T)] for k in range(K)]
buildcapa = [[pulp.LpVariable(f"buildcapa_{k}_{t}", lowBound=0) for t in range(T)] for k in range(K)]
stockhold = [[pulp.LpVariable(f"stockhold_{k}_{t}", lowBound=0) for t in range(T+1)] for k in range(K)]

# Objective function: Maximize total production in the last two years (years 3 and 4)
problem += pulp.lpSum(produce[k][t] for k in range(K) for t in range(2, T))

# Initial stock and capacity constraints
for k in range(K):
    problem += stockhold[k][0] == stock[k]
    problem += produce[k][0] + buildcapa[k][0] <= capacity[k]

# Constraints for each year t and each industry k
for t in range(T):
    for k in range(K):
        if t > 0:
            # Balance constraint for stock
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t-1] - sum(inputone[k][j] * (produce[j][t-1] + buildcapa[j][t-1]) for j in range(K))
        
        # Manpower constraint
        problem += pulp.lpSum(manpowerone[k] * produce[k][t] + manpowertwo[k] * buildcapa[k][t] for k in range(K)) <= manpower_limit

        # Production and building capacity constraint within productive capacity
        problem += produce[k][t] + buildcapa[k][t] <= stockhold[k][t] + stockhold[k][0]

        if t >= 2:
            # Capacity building increase after 2 years
            problem += buildcapa[k][t-2] <= capacity[k]

# Solve the problem
problem.solve()

# Extract the results
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T+1)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')