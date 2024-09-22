import pulp
import json

# Load data from JSON
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

# Define constants
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the LP problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Create decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective function
problem += pulp.lpSum(x[N-1][j] for j in range(N)), "Total_Amount_Currency_N"

# Constraints
# Currency exchange limits
for i in range(N):
    problem += (pulp.lpSum(x[i][j] for j in range(N)) <= limit[i]), f"Limit_Currency_{i}"

# Initial amounts
for i in range(N):
    problem += (start[i] - pulp.lpSum(x[i][j] for j in range(N)) + pulp.lpSum(x[j][i] for j in range(N)) >= 0), f"Initial_Amount_{i}"

# Exchange rates
for i in range(N):
    for j in range(N):
        problem += (x[i][j] <= start[i] * rate[i][j]), f"Exchange_Rate_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')