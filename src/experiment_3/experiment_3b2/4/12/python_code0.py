import pulp
import json

# Input data
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create a problem variable
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective function
objective = start[N-1] + pulp.lpSum([x[i][N-1] * rate[i][N-1] for i in range(N)]) - pulp.lpSum([x[N-1][j] for j in range(N)])
problem += objective

# Constraints
for i in range(N):
    problem += pulp.lpSum([x[i][j] for j in range(N)]) + pulp.lpSum([x[j][i] for j in range(N)]) <= limit[i]

for i in range(N):
    problem += pulp.lpSum([x[i][j] for j in range(N)]) - pulp.lpSum([x[j][i] * rate[j][i] for j in range(N)]) <= start[i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')