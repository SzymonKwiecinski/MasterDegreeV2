import pulp

# Parse the data
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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Currency_N", pulp.LpMaximize)

# Create decision variables
x = [[pulp.LpVariable(f'x_{i}_{j}', lowBound=0) for j in range(N)] for i in range(N)]

# Objective function: Maximize the currency N
problem += pulp.lpSum([x[i][N-1] * rate[i][N-1] for i in range(N)])

# Constraints

# For each currency, total outgoing should be less than available + incoming
for i in range(N):
    problem += (
        pulp.lpSum([x[i][j] for j in range(N)]) - pulp.lpSum([x[j][i] * rate[j][i] for j in range(N)]) <= start[i]
    )

# Apply the exchange limits
for i in range(N):
    for j in range(N):
        problem += x[i][j] <= limit[i]

# Solve the problem
problem.solve()

# Prepare the output
transactions = []
for i in range(N):
    for j in range(N):
        if pulp.value(x[i][j]) > 0:
            transactions.append({
                "from": i + 1,
                "to": j + 1,
                "amount": pulp.value(x[i][j])
            })

final_amount_of_currency_N = sum([pulp.value(x[i][N-1]) * rate[i][N-1] for i in range(N)])

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')