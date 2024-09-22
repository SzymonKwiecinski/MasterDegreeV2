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

K = len(data['capacity'])
T = 5  # Arbitrary choice for number of years

# Problem
problem = pulp.LpProblem("Economic_Planning", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(produce[k, T-2] + produce[k, T-1] for k in range(K))

# Constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            # Initial stock constraint
            problem += stockhold[k, t] == data['stock'][k]
        else:
            # Production and stock constraints
            problem += produce[k, t] + buildcapa[k, t] + stockhold[k, t] == data['capacity'][k] + stockhold[k, t-1]
        
        if t > 0:
            # Input constraints
            problem += pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] + 
                                  data['inputtwo'][k][j] * buildcapa[j, t-1] for j in range(K)) <= data['capacity'][k]

for t in range(T):
    # Manpower constraints
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + 
                          data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit']

for k in range(K):
    for t in range(T-1):
        # Capacity evolution
        problem += buildcapa[k, t] <= data['capacity'][k]  # This line corrected

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')