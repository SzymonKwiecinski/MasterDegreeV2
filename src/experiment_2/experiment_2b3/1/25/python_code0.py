import pulp

# Data from JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'manpower_limit': 470000000.0
}

# Problem parameters
inputone = data["inputone"]
manpowerone = data["manpowerone"]
inputtwo = data["inputtwo"]
manpowertwo = data["manpowertwo"]
stock = data["stock"]
capacity = data["capacity"]
manpower_limit = data["manpower_limit"]

K = len(stock)  # Number of industries
T = 3  # Number of years to plan for

# Initialize the problem
problem = pulp.LpProblem("Economy_Planning", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("Produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("BuildCapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("StockHold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective function
# Maximize total production in the last two years (year 2 and 3 in zero-indexed Python terms)
problem += pulp.lpSum(produce[k, t] for k in range(K) for t in [T-2, T-1])

# Constraints

# Initial stocks and capacity
for k in range(K):
    problem += stockhold[k, 0] == stock[k]
    
# Capacity constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += produce[k, t] <= capacity[k] + stock[k]
        else:
            problem += produce[k, t] <= stockhold[k, t] + sum(buildcapa[k_, t-2] for k_ in range(K)) if t >= 2 else capacity[k]

# Balance equations
for k in range(K):
    for t in range(T):
        if t > 0:
            problem += produce[k, t] + stockhold[k, t-1] == stockhold[k, t] + sum(inputone[k_][k] * produce[k_, t-1] for k_ in range(K)) + sum(inputtwo[k_][k] * buildcapa[k_, t-1] for k_ in range(K))

# Manpower constraints
for t in range(T):
    problem += sum(manpowerone[k] * produce[k, t] + manpowertwo[k] * buildcapa[k, t] for k in range(K)) <= manpower_limit

# Solve the problem
problem.solve()

# Extract results
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)],
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')