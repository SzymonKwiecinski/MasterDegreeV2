from pulp import LpProblem, LpMaximize, LpVariable, lpSum, value
import json

# Load the data
data = '''{'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]], 'manpowerone': [0.6, 0.3, 0.2], 'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]], 'manpowertwo': [0.4, 0.2, 0.1], 'stock': [150, 80, 100], 'capacity': [300, 350, 280], 'demand': [60000000.0, 60000000.0, 30000000.0]}'''
data = json.loads(data.replace("'", "\""))

inputone = data['inputone']
manpowerone = data['manpowerone']
inputtwo = data['inputtwo']
manpowertwo = data['manpowertwo']
stock = data['stock']
capacity = data['capacity']
demand = data['demand']

K = len(inputone)  # Number of industries
T = 5  # Number of years

# Create the LP problem
problem = LpProblem("Maximize_Manpower_Requirement", LpMaximize)

# Decision variables
produce = [[LpVariable(f'produce_{k}_{t}', lowBound=0) for t in range(T)] for k in range(K)]
buildcapa = [[LpVariable(f'buildcapa_{k}_{t}', lowBound=0) for t in range(T)] for k in range(K)]
stockhold = [[LpVariable(f'stockhold_{k}_{t}', lowBound=0) for t in range(T)] for k in range(K)]

# Objective: Maximize the total manpower requirement over five years
problem += lpSum(manpowerone[k] * produce[k][t] + manpowertwo[k] * buildcapa[k][t] for k in range(K) for t in range(T))

# Constraints
for t in range(T):
    for k in range(K):
        # Capacity constraints
        if t == 0:
            problem += produce[k][t] <= capacity[k]
        else:
            problem += produce[k][t] <= capacity[k] + lpSum(buildcapa[k][t-2] for t in range(2, t+1))

        # Stock constraints
        if t == 0:
            problem += stockhold[k][t] == stock[k] + produce[k][t] - buildcapa[k][t]
        else:
            problem += stockhold[k][t] == stockhold[k][t-1] + produce[k][t] - buildcapa[k][t]
        
        # Demand constraints
        if t > 0:
            problem += produce[k][t] >= demand[k]
        
        # Input constraints
        problem += lpSum(inputone[k][j] * produce[j][t] + inputtwo[k][j] * buildcapa[j][t] for j in range(K)) <= stockhold[k][t]

# Solve the problem
problem.solve()

# Prepare the result
result = {
    "produce": [[produce[k][t].varValue for t in range(T)] for k in range(K)],
    "buildcapa": [[buildcapa[k][t].varValue for t in range(T)] for k in range(K)],
    "stockhold": [[stockhold[k][t].varValue for t in range(T)] for k in range(K)]
}

# Output the result
print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')