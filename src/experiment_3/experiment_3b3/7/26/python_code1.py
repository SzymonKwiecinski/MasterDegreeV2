import pulp
import json

# Load data
data = json.loads('{"inputone": [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], "manpowerone": [0.6, 0.3, 0.2], "inputtwo": [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], "manpowertwo": [0.4, 0.2, 0.1], "stock": [150, 80, 100], "capacity": [300, 350, 280], "demand": [60000000.0, 60000000.0, 30000000.0]}')

# Constants from data
inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
demand = data['demand']

K = len(manpowerone)
T = 5

# Define the problem
problem = pulp.LpProblem("MaximizeTotalManpowerRequirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T+1)), lowBound=0, cat='Continuous')
stock_var = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T+1)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(manpowerone[k] * produce[k, t] + manpowertwo[k] * buildcapa[k, t] for k in range(K) for t in range(1, T+1))

# Initial stock condition
for k in range(K):
    stock_var[k, 0] = stock[k]

# Constraints
for t in range(1, T+1):
    for k in range(K):
        # Production constraints
        problem += (produce[k, t] <= 
                    stock_var[k, t-1] + capacity[k] +
                    pulp.lpSum(inputone[k][j] * produce[j, t-1] for j in range(K)) +
                    pulp.lpSum(inputtwo[k][j] * buildcapa[j, t-1] for j in range(K)))  # Changed t-2 to t-1
        
        # Capacity building constraints
        problem += (buildcapa[k, t] <= 
                    stock_var[k, t-1] + 
                    pulp.lpSum(inputtwo[k][j] * produce[j, t-1] for j in range(K)))
        
        # Stock holding constraints
        problem += (stock_var[k, t] == 
                    stock_var[k, t-1] + produce[k, t] - buildcapa[k, t])
        
        # Demand satisfaction constraints
        problem += (produce[k, t] + stock_var[k, t-1] >= demand[k])

# Solve the problem
problem.solve()

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')