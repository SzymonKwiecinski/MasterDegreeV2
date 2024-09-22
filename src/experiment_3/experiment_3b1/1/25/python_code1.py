import pulp
import json

# Data in JSON format
data_json = '''{
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "manpower_limit": 470000000.0
}'''

# Load data
data = json.loads(data_json)

# Parameters
K = len(data['inputone'])  # Number of industries
T = 2  # Total number of years (last two years for production)

# Create the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum([produce[k][1] + produce[k][0] for k in range(K)])

# Production Constraints
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += (produce[k][t] + stockhold[k][t] == 
                         data['capacity'][k])  # Fixed to handle t=0 case
        else:
            problem += (produce[k][t] + stockhold[k][t] == 
                         pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) + 
                         stockhold[k][t] + data['capacity'][k])

# Capacity Building Constraints
for k in range(K):
    problem += (data['capacity'][k] == data['capacity'][k] + 
                 pulp.lpSum(buildcapa[k][t] for t in range(T)))

# Manpower Constraints
for t in range(T):
    problem += (pulp.lpSum(data['manpowerone'][k] * produce[k][t] for k in range(K)) +
                 pulp.lpSum(data['manpowertwo'][k] * buildcapa[k][t] for k in range(K)) 
                 <= data['manpower_limit'])

# Stock Constraints
for k in range(K):
    for t in range(T):
        problem += (stockhold[k][t] == 
                     data['stock'][k] + 
                     pulp.lpSum(produce[k][tt] for tt in range(t)) - 
                     pulp.lpSum(stockhold[k][tt] for tt in range(t)))

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')