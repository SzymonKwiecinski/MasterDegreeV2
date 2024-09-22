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

K = 3  # Number of industries
T = 2  # Number of years, T=2 indicates we consider years 0 and 1

# Create problem
problem = pulp.LpProblem("Industry_Production_and_Capacity", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective
problem += pulp.lpSum(produce[k, T-1] + produce[k, T] for k in range(K))

# Constraints
for t in range(T):
    for k in range(K):
        problem += (pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)) 
                    + pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t-1] for j in range(K)) 
                    <= data['capacity'][k] + stockhold[k, t-1])
        
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t-1] for k in range(K)) 
                <= data['manpower_limit'])

    for k in range(K):
        problem += (stockhold[k, t] == data['capacity'][k] + stockhold[k, t-1] 
                    - pulp.lpSum(data['inputone'][j][k] * produce[j, t] for j in range(K)))

for k in range(K):
    for t in range(T-1):  # capacity constraints for t+2, hence T-1
        problem += (data['capacity'][k] + buildcapa[k, t] == data['capacity'][k] + produce[k, t])

# Initial conditions
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k]
    problem += data['capacity'][k] == data['capacity'][k]

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')