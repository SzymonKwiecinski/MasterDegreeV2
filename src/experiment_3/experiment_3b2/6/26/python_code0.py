import pulp
import json

# Data from the provided JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

# Constants
K = len(data['manpowerone'])  # Number of industries
T = 5  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Economic_Planning", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(1, T + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] 
                      for k in range(K) for t in range(1, T + 1))

# Constraints

# Production and Capacity Constraints
for k in range(K):
    for t in range(1, T + 1):
        problem += (produce[k, t] + buildcapa[k, t] <= 
                     data['capacity'][k] + pulp.lpSum(buildcapa[k, j] for j in range(1, t)),
                     f"Capacity_Constraint_k{k}_t{t}")

# Stock Balance Constraints
for k in range(K):
    problem += stockhold[k, 1] == data['stock'][k] + produce[k, 1] - data['demand'][k] - \
               pulp.lpSum(data['inputone'][k][j] * produce[j, 1] for j in range(K)), f"Stock_Balance_Constraint_k{k}_t1"
    
    for t in range(2, T + 1):
        problem += (stockhold[k, t] == stockhold[k, t - 1] + produce[k, t] - data['demand'][k] - 
                     pulp.lpSum(data['inputone'][k][j] * produce[j, t] for j in range(K)),
                     f"Stock_Balance_Constraint_k{k}_t{t}")

# Non-negativity constraints are inherently defined by the lowBound in the variables

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')