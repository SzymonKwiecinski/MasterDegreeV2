import pulp
import json

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Initialize the problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Decision variables
X = pulp.LpVariable.dicts("X", ((i, j) for i in range(N) for j in range(N)), lowBound=0, cat='Continuous')

# Objective: Maximize currency N at the end of the day
final_currency_N = start[N-1] + pulp.lpSum(X[i, N-1] * rate[i][N-1] for i in range(N) if i != N-1) - pulp.lpSum(X[N-1, j] for j in range(N) if j != N-1)
problem += final_currency_N

# Constraints

# Constraint: Currency amount at the end of the day
for i in range(N):
    problem += pulp.lpSum(X[i, j] for j in range(N)) - pulp.lpSum(X[j, i] * rate[j][i] for j in range(N)) <= limit[i] - start[i]

# Solve the problem
problem.solve()

# Retrieve the output
transactions = [{"from": i+1, "to": j+1, "amount": pulp.value(X[i, j])} for i in range(N) for j in range(N) if pulp.value(X[i, j]) > 0]

# Final amount of currency N
final_amount_of_currency_N = pulp.value(final_currency_N)

# Output result
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')