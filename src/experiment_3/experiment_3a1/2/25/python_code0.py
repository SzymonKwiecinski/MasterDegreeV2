import pulp
import numpy as np

# Data from the provided JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'manpower_limit': 470000000.0
}

K = len(data['capacity'])  # Number of industries
T = 3  # Number of time periods

# Create the problem
problem = pulp.LpProblem("Industry_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[(k, T-1)] + produce[(k, T)] for k in range(K)), "Objective"

# Production Constraints
for k in range(K):
    for t in range(T):
        problem += produce[(k, t)] <= data['capacity'][k] + stock[(k, t)], f"Prod_Capacity_{k}_{t}"

for k in range(K):
    for t in range(1, T):
        problem += stock[(k, t)] == stock[(k, t-1)] + produce[(k, t-1)] - \
                    pulp.lpSum(data['inputone'][j][k] * produce[(j, t-1)] for j in range(K)) + \
                    pulp.lpSum(data['inputtwo'][j][k] * buildcapa[(j, t-2)] for j in range(K)), f"Stock_Balance_{k}_{t}"

# Capacity Building Constraints
for k in range(K):
    for t in range(T):
        problem += buildcapa[(k, t)] <= data['manpower_limit'], f"Build_Manpower_Limit_{k}_{t}"
        
for k in range(K):
    for t in range(2, T):
        problem += buildcapa[(k, t)] <= stock[(k, t-2)], f"Build_Stock_Limit_{k}_{t}"

# Manpower Constraints
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[(k, t)] for k in range(K)) + \
               pulp.lpSum(data['manpowertwo'][k] * buildcapa[(k, t)] for k in range(K)) <= data['manpower_limit'], f"Manpower_Limit_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')