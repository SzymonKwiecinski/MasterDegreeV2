import pandas as pd
import pulp

# Data from JSON
data = {
    'inputone': [[0.1, 0.1, 0.2], [0.5, 0.1, 0.1], [0.5, 0.2, 0.2]],
    'manpowerone': [0.6, 0.3, 0.2],
    'inputtwo': [[0.0, 0.1, 0.2], [0.7, 0.1, 0.1], [0.9, 0.2, 0.2]],
    'manpowertwo': [0.4, 0.2, 0.1],
    'stock': [150, 80, 100],
    'capacity': [300, 350, 280],
    'demand': [60000000.0, 60000000.0, 30000000.0]
}

K = len(data['manpowerone'])  # Number of industries
T = 5  # Number of years

# Create the problem
problem = pulp.LpProblem("Maximize_Manpower", pulp.LpMaximize)

# Decision Variables
produce = pulp.LpVariable.dicts("produce", (range(K), range(1, T+1)), lowBound=0)
buildcapa = pulp.LpVariable.dicts("buildcapa", (range(K), range(1, T+1)), lowBound=0)
stock = pulp.LpVariable.dicts("stock", (range(K), range(T+1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['manpowerone'][k] * produce[k][t] + data['manpowertwo'][k] * buildcapa[k][t] 
                      for k in range(K) for t in range(1, T+1))

# Constraints

# Initial stocks
for k in range(K):
    problem += stock[k][0] == data['stock'][k]

# Production Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += produce[k][t] <= stock[k][t-1] + data['capacity'][k]

# Stock Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += stock[k][t] == stock[k][t-1] + produce[k][t] - data['demand'][k]

# Input Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += (pulp.lpSum(data['inputone'][k][j] * produce[j][t-1] for j in range(K)) + 
                     pulp.lpSum(data['inputtwo'][k][j] * buildcapa[j][t-1] for j in range(K))) <= data['capacity'][k]

# Manpower Constraints
for k in range(K):
    for t in range(1, T+1):
        problem += (data['manpowerone'][k] * produce[k][t] + 
                     data['manpowertwo'][k] * buildcapa[k][t] <= 
                     1)  # Assuming Available Manpower is 1 for the sake of the model

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

for k in range(K):
    for t in range(1, T+1):
        print(f'Produce[{k}][{t}]: {produce[k][t].varValue}, BuildCapa[{k}][{t}]: {buildcapa[k][t].varValue}, Stock[{k}][{t}]: {stock[k][t].varValue}')