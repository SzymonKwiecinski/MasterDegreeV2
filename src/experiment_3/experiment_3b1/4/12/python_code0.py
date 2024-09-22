import pulp
import json

# Given data in JSON format
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

# Parameters
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the Linear Programming problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Decision variables x[i][j] for amount of currency i exchanged for currency j
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective function: Maximize final amount of currency N
final_currency_N = pulp.lpSum(rate[i][N-1] * x[i][N-1] for i in range(N)) + start[N-1] - pulp.lpSum(x[N-1][j] for j in range(N))
problem += final_currency_N, "Objective"

# Constraints for exchange limits
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= limit[i], f"Limit_Constraint_{i}"

# Conservation of currency constraints
final_amounts = [pulp.LpVariable(f"final_amount_{i}", lowBound=0) for i in range(N)]

for i in range(N):
    problem += start[i] - pulp.lpSum(x[i][j] for j in range(N)) + pulp.lpSum(rate[j][i] * x[j][i] for j in range(N)) == final_amounts[i], f"Conservation_Constraint_{i}"

# Specifically for currency N
problem += final_currency_N == start[N-1] + pulp.lpSum(rate[i][N-1] * x[i][N-1] for i in range(N)) - pulp.lpSum(x[N-1][j] for j in range(N)), "Final_Amount_N"

# Solve the problem
problem.solve()

# Output the results
transactions = [(i, j, pulp.value(x[i][j])) for i in range(N) for j in range(N) if pulp.value(x[i][j]) > 0]
final_amount_N = pulp.value(final_currency_N)

print(f'Transactions: {transactions}')
print(f'Final Amount of Currency N: {final_amount_N}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')