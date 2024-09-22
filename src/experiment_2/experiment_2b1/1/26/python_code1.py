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
problem = pulp.LpProblem("MaximizeManpower", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective Function: Maximize total manpower requirement over five years
problem += pulp.lpSum([data['manpowerone'][k] * produce[k][t] for k in range(K) for t in range(T)])

# Constraints

# Demand satisfaction for years 1 to 5
for k in range(K):
    for t in range(1, T):
        problem += produce[k][t] + stockhold[k][t-1] >= data['demand'][k], f"Demand_satisfaction_{k}_{t}"

# Stock constraints: stock at year t = previous stock + produced - demand - build capacity
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += stockhold[k][t] == data['stock'][k] + produce[k][t] - data['demand'][k] if produce[k][t] >= data['demand'][k] else data['stock'][k] + produce[k][t], f"Initial_stock_{k}"
        else:
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t] - data['demand'][k] + buildcapa[k][t-2] if t >= 2 else stockhold[k][t-1] + produce[k][t] - data['demand'][k], f"Stock_constraint_{k}_{t}"

# Capacity constraints for years 1 to 5
for k in range(K):
    for t in range(T):
        problem += produce[k][t] <= data['capacity'][k] + (buildcapa[k][t-1] if t > 0 else 0), f"Capacity_limit_{k}_{t}"

# Input requirements for producing output
for k in range(K):
    for t in range(T):
        for j in range(K):
            if t > 0:  # Ensure we do not access a negative index
                problem += produce[k][t] * data['inputone'][k][j] <= stockhold[j][t-1], f"Input_one_{k}_{j}_{t}"

# Manpower requirements for producing output
for k in range(K):
    for t in range(T):
        problem += produce[k][t] * data['manpowerone'][k] <= 1, f"Manpower_one_{k}_{t}"

# Build capacity constraints
for k in range(K):
    for t in range(T):
        if t >= 2:
            for j in range(K):
                problem += buildcapa[k][t] * data['inputtwo'][k][j] <= stockhold[j][t-1], f"Input_two_{k}_{j}_{t}"
            problem += buildcapa[k][t] * data['manpowertwo'][k] <= 1, f"Manpower_two_{k}_{t}"

# Solve the problem
problem.solve()

# Collect results
produce_result = [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)]
buildcapa_result = [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)]
stockhold_result = [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output results in the required format
output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}