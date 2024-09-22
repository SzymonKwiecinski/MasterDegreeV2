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

K = len(data['capacity'])  # Number of industries
T = 2  # Number of time periods (assuming years)

# Create the problem
problem = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", ((k, t) for k in range(K) for t in range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", ((k, t) for k in range(K) for t in range(T)), lowBound=0)

# Objective Function
problem += pulp.lpSum(produce[k, T-1] + produce[k, T] for k in range(K)), "Total_Production_Last_Two_Years"

# Constraints

# Production Constraints
for k in range(K):
    for t in range(T):
        problem += produce[k, t] <= data['capacity'][k] + (stockhold[k, t-1] if t > 0 else data['stock'][k]), f"Prod_Capacity_Constraint_{k}_{t}"
        
# Input Requirements for Production
for k in range(K):
    for t in range(T):
        problem += produce[k, t] <= pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) + (stockhold[k, t-1] if t > 0 else 0), f"Input_Requirements_{k}_{t}"

# Manpower Constraints
for t in range(T):
    problem += pulp.lpSum(data['manpowerone'][k] * produce[k, t] + data['manpowertwo'][k] * buildcapa[k, t] for k in range(K)) <= data['manpower_limit'], f"Manpower_Constraint_{t}"

# Capacity Building Constraints
for k in range(K):
    for t in range(T):
        problem += buildcapa[k, t] <= pulp.lpSum(data['inputtwo'][k][j] * produce[j, t-1] for j in range(K)), f"Build_Capacity_Constraint_{k}_{t}"

# Stock Balance Equations
for k in range(K):
    for t in range(T):
        problem += stockhold[k, t] == (stockhold[k, t-1] + produce[k, t] - pulp.lpSum(data['inputone'][j][k] * produce[j, t-1] for j in range(K))) if t > 0 else (data['stock'][k] + produce[k, t] - 0), f"Stock_Balance_{k}_{t}"

# Initial Conditions for stockhold
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k], f"Initial_Stock_{k}"

# Run the solver
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')