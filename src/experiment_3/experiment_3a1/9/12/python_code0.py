import pulp
import json

# Data provided in JSON format
data = '{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}'
data = json.loads(data)

# Number of currencies
N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Create the Linear Programming problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Define the decision variables
x = pulp.LpVariable.dicts("exchange", (range(N), range(N)), lowBound=0)  # x[i][j] amounts exchanged from i to j
y = pulp.LpVariable.dicts("hold", range(N), lowBound=0)  # y[i] amounts held after transactions

# Objective Function
problem += y[N-1], "Maximize_Amount_of_Currency_N"

# Constraints
# 1. Initial Currency Holdings
for i in range(N):
    problem += (y[i] == Start[i] + pulp.lpSum(x[j][i] for j in range(N)) - pulp.lpSum(x[i][j] for j in range(N))), f"Initial_Holdings_Constraint_{i}"

# 2. Currency Exchange Limits
for i in range(N):
    problem += (pulp.lpSum(x[i][j] for j in range(N)) + pulp.lpSum(x[j][i] for j in range(N)) <= Limit[i]), f"Exchange_Limits_Constraint_{i}"

# 3. Exchange Rates
for i in range(N):
    for j in range(N):
        problem += (x[i][j] <= Rate[i][j] * y[i]), f"Exchange_Rate_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')