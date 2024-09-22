import pulp
import json

# Input data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
    'manpowerone': [0.6, 0.3, 0.2], 
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
    'manpowertwo': [0.4, 0.2, 0.1], 
    'stock': [150, 80, 100], 
    'capacity': [300, 350, 280], 
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['inputone'])  # Number of industries
T = 5  # Number of years

# Create the LP problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", [(k, t) for k in range(K) for t in range(T)], lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", [(k, t) for k in range(K) for t in range(T)], lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", [(k, t) for k in range(K) for t in range(T)], lowBound=0)

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * (pulp.lpSum(produce[k, t] for t in range(T)) + 
                                                  pulp.lpSum(buildcapa[k, t] for t in range(T)) 
                                                  for k in range(K))), "Total_Manpower_Requirement"

# Constraints
for t in range(T):
    for k in range(K):
        # Stock and production constraints
        if t > 0:
            problem += stockhold[k, t-1] + produce[k, t] - pulp.lpSum(data['inputone'][k][j] * produce[j, t-1] for j in range(K)) == stockhold[k, t], f"Stock_Constraint_{k}_{t}"
        if t > 1:
            problem += stockhold[k, t-2] + buildcapa[k, t-1] - pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j, t-2] for j in range(K)) == stockhold[k, t], f"Build_Stock_Constraint_{k}_{t}"
        
        # Demand satisfaction
        problem += produce[k, t] + stockhold[k, t] >= data['demand'][k], f"Demand_Constraint_{k}_{t}"

        # Capacity constraints
        problem += produce[k, t] <= data['capacity'][k], f"Capacity_Constraint_{k}_{t}"
        problem += buildcapa[k, t] <= data['capacity'][k], f"Build_Capacity_Constraint_{k}_{t}"

# Initial stock conditions
for k in range(K):
    problem += stockhold[k, 0] == data['stock'][k], f"Initial_Stock_Condition_{k}"

# Solve the problem
problem.solve()

# Prepare output format
output = {
    "produce": [[pulp.value(produce[k, t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k, t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k, t]) for t in range(T)] for k in range(K)]
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')