import pulp
import json

# Data provided in JSON format
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

# Parameters
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the problem variable
problem = pulp.LpProblem("Maximize_Currency", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0)

# Objective Function
problem += x[(N-1, N-1)] + pulp.lpSum(x[(N-1, j)] for j in range(N)), "Objective"

# Constraints
# Exchange Limits
for i in range(N):
    problem += pulp.lpSum(x[(i, j)] for j in range(N)) <= limit[i], f"Limit_Constraint_{i}"

# Initial Constraints
for i in range(N):
    problem += x[(i, i)] + pulp.lpSum(x[(j, i)] for j in range(N)) <= start[i], f"Start_Constraint_{i}"

# Exchange Rate Constraints
for i in range(N):
    for j in range(N):
        problem += x[(i, j)] <= rate[i][j] * pulp.lpSum(x[(k, i)] for k in range(N)), f"Rate_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')