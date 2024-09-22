import pulp
import json

# Data
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the problem
problem = pulp.LpProblem("CurrencyExchange", pulp.LpMaximize)

# Decision variables: x[i][j] for amount exchanged from currency i to currency j
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective function: maximize final currency N
final_currency_N = start[2] + pulp.lpSum(x[j][2] for j in range(N))
problem += final_currency_N, "MaximizeFinalCurrencyN"

# Constraints
# 1. Exchange limits for each currency
for i in range(N):
    problem += (pulp.lpSum(x[i][j] for j in range(N)) - 
                 pulp.lpSum(x[j][i] for j in range(N)) <= limit[i]), f"ExchangeLimit_{i}"

# 2. Wealth preservation constraints
for i in range(N):
    problem += (pulp.lpSum(x[i][j] / rate[i][j] for j in range(N)) <= start[i]), f"WealthPreservation_{i}"

# Solve the problem
problem.solve()

# Collect output information
transactions = []
for i in range(N):
    for j in range(N):
        if pulp.value(x[i][j]) > 0:
            transactions.append({'from': i, 'to': j, 'amount': pulp.value(x[i][j])})

# Final amount of currency N
final_amount_of_currency_N = pulp.value(final_currency_N)

# Print results
print(f'Transactions: {transactions}')
print(f'Final amount of currency N: {final_amount_of_currency_N}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')