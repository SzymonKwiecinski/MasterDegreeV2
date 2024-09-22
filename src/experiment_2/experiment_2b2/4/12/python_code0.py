import pulp

# Input data
data = {
    'N': 3,
    'Start': [100.0, 50.0, 200.0],
    'Limit': [1000.0, 200.0, 3000.0],
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Initialize the linear programming problem
problem = pulp.LpProblem("Maximize_Final_Currency", pulp.LpMaximize)

# Decision variables: amount_ij is the amount to be exchanged from currency i to currency j
amount = {
    (i, j): pulp.LpVariable(f'amount_{i}_{j}', lowBound=0)
    for i in range(N) for j in range(N)
}

# Objective: Maximize the final amount of currency N-1
final_amount_currency_N = start[N-1] + sum(amount[i, N-1] * rate[i][N-1] for i in range(N))
problem += final_amount_currency_N

# Constraints:

# 1. Exchanges made should not exceed the start amount plus the received amount
for i in range(N):
    problem += sum(amount[i, j] for j in range(N)) <= start[i] + sum(amount[j, i] * rate[j][i] for j in range(N))

# 2. Respect the limit regulations
for i in range(N):
    problem += sum(amount[i, j] for j in range(N)) <= limit[i]

# Solve the problem
problem.solve()

# Retrieve the resulting transactions
transactions = [
    {
        "from": i,
        "to": j,
        "amount": pulp.value(amount[i, j])
    }
    for i in range(N) for j in range(N) if pulp.value(amount[i, j]) > 0
]

# Final amount of currency N
final_currency_N_value = pulp.value(final_amount_currency_N)

# Output result
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_currency_N_value
}

import json
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')