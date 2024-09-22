import pulp
import json

# Data input
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the problem
problem = pulp.LpProblem("Maximize_Currency_N", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("exchange", (range(N), range(N)), lowBound=0)

# Objective function
problem += x[N-1][N-1] + pulp.lpSum(x[N-1][j] * rate[N-1][j] for j in range(N)), "Total Amount of Currency N"

# Constraints
# Exchange Amount Constraints
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= limit[i], f"Limit_Constraint_{i}"

# Starting Amount Constraints
for i in range(N):
    for j in range(N):
        problem += x[i][j] <= start[i], f"Start_Constraint_{i}_{j}"

# Exchange Rate Constraints
for i in range(N):
    for j in range(N):
        if i != j:
            problem += x[i][j] * rate[i][j] <= x[j][i], f"Rate_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')