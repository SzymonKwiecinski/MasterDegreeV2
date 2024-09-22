import pulp
import json

# Data in JSON format
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 
        'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

# Variables
N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Exchange_Profit", pulp.LpMaximize)

# Decision variables: x[i][j]
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective function
problem += pulp.lpSum(x[i][N-1] * Rate[i][N-1] for i in range(N))

# Exchange Limits
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= Limit[i]

# Currency Conservation
for i in range(N):
    problem += Start[i] + pulp.lpSum(x[j][i] * Rate[j][i] for j in range(N)) - pulp.lpSum(x[i][j] for j in range(N)) >= 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')