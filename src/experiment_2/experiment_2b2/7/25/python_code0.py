import pulp

# Data provided in the JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

# Initializing parameters
inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
manpower_limit = data['manpower_limit']

K = len(capacity)  # Number of industries

# Defining the problem
problem = pulp.LpProblem("Maximize_Total_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(4)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(4)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(4)), lowBound=0)

# Objective Function: Maximize total production in the last two years
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in range(2, 4))

# Constraints

# Capacity constraints
for k in range(K):
    problem += produce[k, 0] <= capacity[k]

# Manpower constraints
for t in range(4):
    problem += pulp.lpSum(manpowerone[k] * produce[k, t] + manpowertwo[k] * buildcapa[k, t] for k in range(K)) <= manpower_limit

# Stock, Production and Building constraints over time
for k in range(K):
    for t in range(1, 4):
        required_inputs = pulp.lpSum(inputone[k][j] * produce[j, t - 1] for j in range(K))
        capacity_increase = 0
        if t >= 2:
            capacity_increase += buildcapa[k, t - 2]

        problem += stockhold[k, t - 1] + capacity_increase + produce[k, t] + buildcapa[k, t] <= stockhold[k, t] + required_inputs

# Initial stock condition
for k in range(K):
    problem += stockhold[k, 0] == stock[k] - produce[k, 0] - buildcapa[k, 0]

# Solve the problem
problem.solve()

# Prepare the output data
output_data = {
    "produce": [[pulp.value(produce[k, t]) for t in range(4)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(4)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(4)] for k in range(K)]
}

print(output_data)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')