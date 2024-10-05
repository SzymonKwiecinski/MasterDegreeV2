import pulp

# Data
inputone = [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]]
manpowerone = [0.6, 0.3, 0.2]
inputtwo = [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]]
manpowertwo = [0.4, 0.2, 0.1]
initial_stock = [150, 80, 100]
initial_capacity = [300, 350, 280]
demand = [60000000.0, 60000000.0, 30000000.0]

K = len(demand)
T = 5

# Problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T+1)), lowBound=0)

# Initial capacity and stock
for k in range(K):
    stockhold[k][0] = initial_stock[k]

# Objective function
problem += pulp.lpSum(manpowerone[k] * produce[k][t] + manpowertwo[k] * buildcapa[k][t] for k in range(K) for t in range(T))

# Constraints
for k in range(K):
    for t in range(T):
        # Demand Satisfaction
        if t == 0:
            problem += produce[k][t] + initial_stock[k] - stockhold[k][t+1] >= demand[k]
        else:
            problem += produce[k][t] + stockhold[k][t] - stockhold[k][t+1] >= demand[k]
        
        # Input Requirements
        if t == 0:
            problem += pulp.lpSum(inputone[k][j] * produce[j][t] for j in range(K)) + pulp.lpSum(inputtwo[k][j] * buildcapa[j][t] for j in range(K)) <= initial_capacity[k]
        elif t >= 2:
            problem += pulp.lpSum(inputone[k][j] * produce[j][t] for j in range(K)) + pulp.lpSum(inputtwo[k][j] * buildcapa[j][t] for j in range(K)) <= initial_capacity[k] + buildcapa[k][t-2]
        else:
            problem += pulp.lpSum(inputone[k][j] * produce[j][t] for j in range(K)) + pulp.lpSum(inputtwo[k][j] * buildcapa[j][t] for j in range(K)) <= initial_capacity[k]

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')