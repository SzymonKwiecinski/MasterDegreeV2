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

# Create the problem instance
problem = pulp.LpProblem("Maximize_Manpower_Requirement", pulp.LpMaximize)

# Decision variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(T)), lowBound=0, cat='Continuous')
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(T)), lowBound=0, cat='Continuous')
stockhold = pulp.LpVariable.dicts("stockhold", (range(K), range(T)), lowBound=0, cat='Continuous')

# Objective function: maximize total manpower requirement over five years
problem += pulp.lpSum(data['manpowerone'][k] * (produce[k][t] + buildcapa[k][t]) for k in range(K) for t in range(T))

# Constraints for stock and capacity
for k in range(K):
    for t in range(T):
        if t == 0:
            problem += stockhold[k][t] == data['stock'][k] - produce[k][t]  # year 0 stock constraint
        else:
            problem += stockhold[k][t] == stockhold[k][t-1] + buildcapa[k][t-1] - produce[k][t]  # stock from previous year
            
        # Capacity constraints
        if t > 0:
            problem += produce[k][t] <= data['capacity'][k] + buildcapa[k][t-2]  # capacity from year t-2
        
        # Demand constraints
        problem += produce[k][t] >= data['demand'][k]

# Add manpower constraints based on input requirements
for k in range(K):
    for t in range(T):
        for j in range(K):
            if t > 0:
                problem += produce[k][t] >= data['inputone'][k][j] * produce[j][t-1]  # input from other industries

# Solve the problem
problem.solve()

# Output results
produce_result = [[pulp.value(produce[k][t]) for t in range(T)] for k in range(K)]
buildcapa_result = [[pulp.value(buildcapa[k][t]) for t in range(T)] for k in range(K)]
stockhold_result = [[pulp.value(stockhold[k][t]) for t in range(T)] for k in range(K)]

output = {
    "produce": produce_result,
    "buildcapa": buildcapa_result,
    "stockhold": stockhold_result
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')