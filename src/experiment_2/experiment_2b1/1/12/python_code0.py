import pulp
import json

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Initialize the problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Decision variables for amounts exchanged
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective function: maximize the total final amount of currency N
final_amount_currency_N = pulp.lpSum([start[i] - pulp.lpSum([x[i][j] for j in range(N)]) + pulp.lpSum([x[j][i] for j in range(N)]) for i in range(N)]) + x[N-1][N-1]
problem += pulp.lpSum([x[N-1][j] for j in range(N)])  # we want to maximize currency N at final

# Constraints: limits on the currency exchanges
for i in range(N):
    problem += pulp.lpSum([x[i][j] for j in range(N)]) <= limit[i]
    problem += pulp.lpSum([x[j][i] for j in range(N)]) <= limit[i]

# Constraints on the exchanged amounts based on rates
for i in range(N):
    for j in range(N):
        if i != j:
            problem += x[i][j] <= start[i] * rate[i][j]

# Solve the problem
problem.solve()

# Prepare the transactions output
transactions = []
for i in range(N):
    for j in range(N):
        if i != j and pulp.value(x[i][j]) > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": pulp.value(x[i][j])
            })

# Final amount of currency N
final_amount_currency_N_value = sum([start[i] - pulp.value(pulp.lpSum([x[i][j] for j in range(N)])) + pulp.value(pulp.lpSum([x[j][i] for j in range(N)])) for i in range(N)]) + pulp.value(x[N-1][N-1])

# Output result
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_currency_N_value
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')