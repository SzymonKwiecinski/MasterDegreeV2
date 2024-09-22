import pulp
import json

# Data provided in JSON format
data_json = """{
    "inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    "manpowerone": [0.6, 0.3, 0.2],
    "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    "manpowertwo": [0.4, 0.2, 0.1],
    "stock": [150, 80, 100],
    "capacity": [300, 350, 280],
    "demand": [60000000.0, 60000000.0, 30000000.0]
}"""

data = json.loads(data_json)

K = len(data['manpowerone'])  # Number of industries
T = 5  # Time period

# Create the problem instance
problem = pulp.LpProblem("Industry_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", (k for k in range(K)), lowBound=0)  # Initial stock variables

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] 
                       for k in range(K) for t in range(1, T + 1))

# Constraints
# Production constraints
for k in range(K):
    for t in range(1, T + 1):
        if t == 1:
            problem += (produce[k, t] + data['stock'][k] == 
                         pulp.lpSum(data['inputone'][k][j] * produce[j, 1] for j in range(K)) + 
                         stock[k] + buildcapa[k, 0])
        else:
            problem += (produce[k, t] + stock[k] == 
                         pulp.lpSum(data['inputone'][k][j] * produce[j, t - 1] for j in range(K)) + 
                         stock[k] + buildcapa[k, t - 1])
    
# Capacity building constraints
for k in range(K):
    problem += (pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t] for j in range(K) for t in range(1, T + 1)) <= 
                 data['capacity'][k] + stock[k])
    
# Demand satisfaction constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += (produce[k, t] + stock[k] >= data['demand'][k])

# Solve the problem
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')