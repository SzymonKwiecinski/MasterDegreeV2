import pulp

# Data extracted from the provided JSON format
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

K = len(data['stock'])
T = 2  # Given T from the problem statement

# Initialize the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T+1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T+1)), lowBound=0)

# Objective Function
problem += pulp.lpSum([produce[k][T-1] + produce[k][T] for k in range(K)])

# Constraints
for t in range(T+1):
    for k in range(K):
        # Production Constraint
        problem += produce[k][t] <= data['capacity'][k] + (stockhold[k][t-1] if t > 0 else data['stock'][k]), f"ProdConstraint_{k}_{t}"
        
        # Input Requirement
        problem += (pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) +
                     (stockhold[k][t-1] if t > 0 else 0) >= produce[k][t]), f"InputRequirement_{k}_{t}"
        
        # Capacity Building
        problem += buildcapa[k][t] <= data['capacity'][k] + (stockhold[k][t-1] if t > 0 else data['stock'][k]), f"BuildCapa_{k}_{t}"

# Manpower Constraints
for t in range(T+1):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K)) +
                pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) <= data['manpower_limit']), f"ManpowerConstraint_{t}"

for t in range(1, T+1):
    for k in range(K):
        # Stock Dynamics
        problem += (stockhold[k][t] == (stockhold[k][t-1] if t > 1 else data['stock'][k]) +
                     produce[k][t-1] - pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) -
                     buildcapa[k][t]), f"StockDynamics_{k}_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')