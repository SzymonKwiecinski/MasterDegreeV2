import pulp

# Data from the JSON input
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

# Problem data
K = len(data['inputone'])
T = 5 

# Initializing the problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0)

# Objective
total_manpower = sum(
    data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] 
    for k in range(K) for t in range(T)
)
problem += total_manpower

# Constraints

# Capacity constraints
for k in range(K):
    for t in range(T):
        effective_capacity = data['capacity'][k]
        if t >= 1:
            effective_capacity += buildcapa[k, t-1]
        problem += (produce[k, t] + stockhold[k, t] <= effective_capacity, f"capacity_{k}_{t}")

# Supply-Demand balance and stock constraints
for k in range(K):
    problem += (stockhold[k, 0] == data['stock'][k], f"initial_stock_{k}")
    for t in range(T):
        if t >= 1:
            total_input_one = sum(data['inputone'][k][j] * produce[j, t] for j in range(K))
            problem += (produce[k, t] + stockhold[k, t-1] >= data['demand'][k] + total_input_one + stockhold[k, t], f"supply_demand_balance_{k}_{t}")

# Input constraints for building capacity
for k in range(K):
    for t in range(T-2):
        total_input_two = sum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K))
        for j in range(K):
            problem += (total_input_two <= produce[j, t], f"input_constraint_{k}_{j}_{t}")

# Solve the problem
problem.solve()

# Output construction
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T + 1)] for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')