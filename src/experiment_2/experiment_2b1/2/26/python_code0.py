import pulp
import json

# Input data
data = {'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 
        'manpowerone': [0.6, 0.3, 0.2], 
        'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 
        'manpowertwo': [0.4, 0.2, 0.1], 
        'stock': [150, 80, 100], 
        'capacity': [300, 350, 280], 
        'demand': [60000000.0, 60000000.0, 30000000.0]}

K = len(data['inputone'])  # Number of industries
T = 5  # Number of years

# Create the problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Define decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective function: Maximize the total manpower requirement over five years
manpower_requirement = pulp.lpSum(data['manpowerone'][k] * (produce[k][t] + buildcapa[k][t]) for k in range(K) for t in range(T))
problem += manpower_requirement

# Constraints
for k in range(K):
    for t in range(T):
        # Stock balance
        if t == 0:
            problem += stockhold[k][t] == data['stock'][k] + produce[k][t]
        else:
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t]
        
        # Demand satisfaction
        problem += produce[k][t] + stockhold[k][t] >= data['demand'][k]

        # Capacity of industry k
        if t < T - 1:
            problem += produce[k][t] <= data['capacity'][k] + buildcapa[k][t]

        # Build capacity constraints
        problem += buildcapa[k][t] <= data['capacity'][k] - stockhold[k][t]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "produce": [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)],
    "buildcapa": [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)],
    "stockhold": [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]
}

# Print the output and objective value
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')