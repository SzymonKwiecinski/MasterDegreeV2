import pulp
import json

data = {'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
        'manpowerone': [0.6, 0.3, 0.2], 
        'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
        'manpowertwo': [0.4, 0.2, 0.1], 
        'stock': [150, 80, 100], 
        'capacity': [300, 350, 280], 
        'demand': [60000000.0, 60000000.0, 30000000.0]}

K = len(data['demand'])  # Number of industries
T = 5  # Number of years

# Create the problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective function: maximize total manpower requirement
problem += pulp.lpSum(data['manpowerone'][k] * (produce[k][t] + buildcapa[k][t]) for k in range(K) for t in range(T)), "Total_Manpower_Requirement"

# Constraints
for t in range(T):
    for k in range(K):
        # Demand constraints
        if t > 0:
            problem += produce[k][t] + stockhold[k][t-1] - stockhold[k][t] == data['demand'][k], f"Demand_Constraint_{k}_{t}"
        
        # Capacity constraints
        if t > 0:
            problem += produce[k][t] <= data['capacity'][k] + (buildcapa[k][t-2] if t > 1 else 0), f"Capacity_Constraint_{k}_{t}"

        # Input constraints for production
        if t > 0:
            problem += produce[k][t] <= pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) + data['stock'][k], f"Input_One_Constraint_{k}_{t}"

        # Input constraints for building capacity
        problem += buildcapa[k][t] <= pulp.lpSum(data['inputtwo'][k][j] * produce[j][t-1] for j in range(K)), f"Input_Two_Constraint_{k}_{t}"

# Solve the problem
problem.solve()

# Format results
produce_result = [[produce[k][t].varValue for t in range(T)] for k in range(K)]
buildcapa_result = [[buildcapa[k][t].varValue for t in range(T)] for k in range(K)]
stockhold_result = [[stockhold[k][t].varValue for t in range(T)] for k in range(K)]

# Print the results with objective value
output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')