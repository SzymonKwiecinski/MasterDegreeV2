import pulp

# Data from the JSON input
data = {'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
        'manpowerone': [0.6, 0.3, 0.2], 
        'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
        'manpowertwo': [0.4, 0.2, 0.1], 
        'stock': [150, 80, 100], 
        'capacity': [300, 350, 280], 
        'demand': [60000000.0, 60000000.0, 30000000.0]}

# Extracting data
inputone = data["inputone"]
manpowerone = data["manpowerone"]
inputtwo = data["inputtwo"]
manpowertwo = data["manpowertwo"]
stock = data["stock"]
capacity = data["capacity"]
demand = data["demand"]

K = len(inputone)  # Number of industries
T = 5  # Consider 5 years from year 0 to year 4

# Create the LP problem
problem = pulp.LpProblem("Maximize_Total_Manpower", pulp.LpMaximize)

# Define variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Resetting objective to avoid overwriting warning
problem += 0  # Initialize the objective to zero

# Objective function: Maximize total manpower requirement
problem += pulp.lpSum([produce[k, t] * manpowerone[k] + buildcapa[k, t] * manpowertwo[k] for k in range(K) for t in range(T)])

# Constraints
for k in range(K):
    for t in range(T):
        inputs = pulp.lpSum([produce[j, t] * inputone[k][j] + buildcapa[j, t] * inputtwo[k][j] for j in range(K)])
        if t == 0:
            problem += produce[k, t] <= capacity[k] + stock[k] - inputs
        else:
            problem += produce[k, t] <= stockhold[k, t-1] + capacity[k] + pulp.lpSum([buildcapa[k, t-2] if t-2 >= 0 else 0 for k in range(K)]) - inputs
            
        problem += stockhold[k, t] == stockhold[k, t-1] + produce[k, t] - buildcapa[k, t] - demand[k] if t > 0 else stock[k] + produce[k, t] - buildcapa[k, t] - demand[k]

# Solve the problem
problem.solve()

# Collect the results
produce_result = [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)]
buildcapa_result = [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)]
stockhold_result = [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]

output_result = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

print(output_result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')