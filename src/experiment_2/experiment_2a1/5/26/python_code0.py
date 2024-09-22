import pulp
import json

# Input Data
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['inputone'])   # Number of industries
T = 5                       # Time horizon (5 years)

# Define the problem
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0)
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0)

# Objective function
problem += pulp.lpSum(data['manpowerone'][k] * pulp.lpSum(produce[k][t] for t in range(T)) +
                      data['manpowertwo'][k] * pulp.lpSum(buildcapa[k][t] for t in range(T)) for k in range(K))

# Constraints
for t in range(T):
    for k in range(K):
        # Stock balance constraint
        if t == 0:
            problem += stockhold[k][t] == data['stock'][k] + produce[k][t] - data['demand'][k]
        else:
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t] - data['demand'][k]
        
        # Capacity constraint
        problem += produce[k][t] <= data['capacity'][k] + pulp.lpSum(buildcapa[m][t-1] * data['inputtwo'][m][k] for m in range(K)) if t > 0 else 0
    
        # Build capacity constraint
        if t < T - 1:  # Can't build capacity in last year
            problem += buildcapa[k][t] <= stockhold[k][t] // data['inputtwo'][k][k]
  
# Solve the problem
problem.solve()

# Prepare the output
produce_result = [[produce[k][t].varValue for t in range(T)] for k in range(K)]
buildcapa_result = [[buildcapa[k][t].varValue for t in range(T)] for k in range(K)]
stockhold_result = [[stockhold[k][t].varValue for t in range(T)] for k in range(K)]

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output result
output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}