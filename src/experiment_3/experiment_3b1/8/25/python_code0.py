import pulp
import numpy as np

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

# Model parameters
K = len(data['stock'])  # Number of industries
T = 3  # Number of years considered, last two years are T-1 and T

# Initialize the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k, T-1] + produce[k, T] for k in range(K)), "Total_Production"

# Constraints

# Production Constraints for Year t
for k in range(K):
    for t in range(T):
        problem += produce[k, t] <= data['capacity'][k] + stock[k, t-1] if t > 0 else data['capacity'][k] + data['stock'][k]

# Manpower Constraints for Production
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] for k in range(K)) <= data['manpower_limit'], f"Manpower_Production_Year_{t}"

# Input Constraints for Production
for k in range(K):
    for t in range(T):
        if t > 0:
            problem += pulp.lpSum(data['inputone'][k][j] * produce[k, t] for j in range(K)) <= stock[j][t-1] + buildcapa[j][t-2] if t > 1 else 0, f"Input_Production_{k}_Year_{t}"

# Capacity Building Constraints for Year t
for k in range(K):
    for t in range(T):
        problem += buildcapa[k, t] <= data['capacity'][k] + stock[k, t-1] if t > 0 else data['capacity'][k] + data['stock'][k]

# Manpower Constraints for Capacity Building
for t in range(T):
    problem += pulp.lpSum(data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'], f"Manpower_Building_Year_{t}"

# Stock Dynamics
for k in range(K):
    for t in range(1, T):
        problem += stock[k, t] == stock[k, t-1] + produce[k, t-1] - pulp.lpSum(data['inputone'][j][k] * produce[j, t-1] for j in range(K)) + buildcapa[k, t-2] if t > 1 else 0, f"Stock_Dynamics_{k}_Year_{t}"

# Solve the problem
problem.solve()

# Output the results
produce_matrix = np.zeros((K, T))
buildcapa_matrix = np.zeros((K, T))
stockhold_matrix = np.zeros((K, T))

for k in range(K):
    for t in range(T):
        produce_matrix[k][t] = pulp.value(produce[k, t])
        buildcapa_matrix[k][t] = pulp.value(buildcapa[k, t])
        stockhold_matrix[k][t] = pulp.value(stock[k, t])

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')