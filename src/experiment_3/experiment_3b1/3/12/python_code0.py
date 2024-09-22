import pulp
import json

# Data input
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Define the problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("exchange", (range(N), range(N)), lowBound=0)

# Objective function: maximize the total amount of currency N
problem += pulp.lpSum(x[N-1][j] for j in range(N) if j != N-1), "Objective"

# Constraints
# Currency Exchange Limits
for i in range(N):
    for j in range(N):
        problem += x[i][j] <= limit[i], f"Limit_{i}_{j}"

# Initial Currency Constraints
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= start[i], f"StartConstraint_{i}"

# Total Exchange Calculation
for i in range(N):
    for j in range(N):
        problem += x[i][j] <= start[i] * rate[i][j], f"RateConstraint_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')