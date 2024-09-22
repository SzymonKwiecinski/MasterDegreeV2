import pulp

# Input data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0],
    'total_manpower': 1000000.0  # Assuming total manpower available is constant for simplicity
}

K = len(data['demand'])
T = 5  # Number of years

# Initialize problem
problem = pulp.LpProblem("Economic_Production_and_Capacity_Building", pulp.LpMaximize)

# Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t]
                      for k in range(K) for t in range(1, T+1))

# Constraints

# Initial stock constraints
for k in range(K):
    stock[k, 0] = data['stock'][k]

# Production and demand constraints
for k in range(K):
    for t in range(1, T+1):
        problem += produce[k, t] + stock[k, t-1] == data['demand'][k] + stock[k, t]

# Input requirements for production
for k in range(K):
    for t in range(1, T+1):
        problem += pulp.lpSum(data['inputone'][k][j] * produce[j, max(0, t-1)] for j in range(K)) + stock[k, t-1] >= produce[k, t]

# Building capacity constraints
for k in range(K):
    for t in range(1, T+1):
        problem += pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K)) <= data['capacity'][k]

# Manpower availability constraints
for t in range(1, T+1):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['total_manpower']

# Capacity increment constraints
for k in range(K):
    for t in range(1, T-1):
        problem += data['capacity'][k] + pulp.lpSum(buildcapa[k, year] for year in range(1, t+1)) >= produce[k, t+2]

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')