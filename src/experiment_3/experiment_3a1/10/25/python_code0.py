import pulp
import json

# Data in JSON format
data = '''{
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    "manpowerone": [0.6, 0.3, 0.2], 
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    "manpowertwo": [0.4, 0.2, 0.1], 
    "stock": [150, 80, 100], 
    "capacity": [300, 350, 280], 
    "manpower_limit": 470000000.0
}'''
data = json.loads(data)

# Model Parameters
K = len(data['manpowerone'])  # Number of industries
T = 2  # Time horizon (last two years are T-1 and T)

# Create the LP problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", (k for k in range(K)), lowBound=0)

# Objective Function
problem += pulp.lpSum([produce[k, T-1] + produce[k, T] for k in range(K)])

# Constraints
# Production Constraints
for k in range(K):
    for t in range(T):
        problem += produce[k, t] <= data['capacity'][k] + (stock[k] if t == 0 else stock[k])

# Input Requirements for Production
for k in range(K):
    for t in range(T):
        inputs = pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K))
        problem += inputs + data['manpowerone'][k] * produce[k, t] <= stock[k] + data['capacity'][k]

# Manpower Constraints
for t in range(T):
    manpower_used = pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) + \
                    pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K))
    problem += manpower_used <= data['manpower_limit']

# Capacity Building Constraints
for k in range(K):
    for t in range(T):
        problem += buildcapa[k, t] <= stock[k]

# Stock Dynamics
for k in range(K):
    for t in range(1, T):
        problem += stock[k] == stock[k] + produce[k, t] - \
                   pulp.lpSum(data['inputone'][j][k] * produce[j, t-1] for j in range(K)) - buildcapa[k, t]

# Initial Conditions at year 0
for k in range(K):
    stock[k] = data['stock'][k]
    capacity = data['capacity'][k]

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')