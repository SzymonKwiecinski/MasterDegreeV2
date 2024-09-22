import pulp
import json

# Input data
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

# Parameters from the data
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the problem
problem = pulp.LpProblem("CurrencyExchange", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), 0)  # amount exchanged from i to j
y = pulp.LpVariable.dicts("y", range(N), 0)  # amount kept of currency i

# Objective Function
problem += pulp.lpSum(y[j] for j in range(N)), "TotalCurrencyKept"

# Constraints

# Exchange Limit Constraints
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= limit[i], f"Limit_Constraint_{i}"

# Initial Amount Constraints
for i in range(N):
    problem += y[i] + pulp.lpSum(x[i, j] for j in range(N)) == start[i], f"Initial_Amount_Constraint_{i}"

# Wealth Cycle Constraint
for i in range(N):
    problem += pulp.lpSum(x[i, j] * rate[i][j] for j in range(N)) <= y[i], f"Wealth_Cycle_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')