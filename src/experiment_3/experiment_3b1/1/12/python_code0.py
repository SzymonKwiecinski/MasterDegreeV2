import pulp
import json

# Data in JSON format
data = '{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}'
params = json.loads(data)

# Extract parameters
N = params['N']
starts = params['Start']
limits = params['Limit']
rates = params['Rate']

# Create a linear programming problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Create decision variables
x = pulp.LpVariable.dicts("exchange", (range(N), range(N)), lowBound=0)

# Objective function: Maximize final amount of currency N
problem += pulp.lpSum(x[N-1][j] for j in range(N)), "Maximize_Financial_Gain"

# Constraints
# Exchange limits for each currency
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= limits[i], f"Limit_Constraint_{i}"

# Initial amounts
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= starts[i], f"Start_Constraint_{i}"

# Wealth cannot be multiplied through cycles (non-cyclical exchange is assumed)
# This can be implicitly checked through exchange rate conditions

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')