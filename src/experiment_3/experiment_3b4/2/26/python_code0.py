import pulp

# Load data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['inputone'])  # Number of industries
T = 5  # Number of years

# Create the Linear Programming Problem
problem = pulp.LpProblem("Maximize_Manpower_Usage", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective Function: Maximize total manpower usage over T years
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t]
                      for k in range(K) for t in range(T))

# Constraints

# Initial stock constraints
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k]

# Production capacity constraints
for k in range(K):
    for t in range(T):
        problem += produce[k, t] + buildcapa[k, t] <= data['capacity'][k] + pulp.lpSum(buildcapa[k, tau] for tau in range(t))

# Stock balance constraints
for k in range(K):
    for t in range(1, T):
        problem += stockhold[k, t] == stockhold[k, t-1] + produce[k, t] - \
                   pulp.lpSum(data['inputone'][j][k] * produce[j, t] for j in range(K)) - \
                   data['demand'][k]

# Solve the problem
problem.solve()

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')