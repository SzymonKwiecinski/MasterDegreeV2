import pulp

# Parse the input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the LP problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Decision variables: x_ij is the amount of currency i exchanged for currency j
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0, cat=pulp.LpContinuous)

# Objective: Maximize the final amount of currency N
problem += pulp.lpSum(x[i][N-1] * rate[i][N-1] for i in range(N))

# Constraints
for i in range(N):
    # Total amount exchanged from currency i should not exceed the start amount plus inflows
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= start[i] + pulp.lpSum(x[j][i] * rate[j][i] for j in range(N))
    # Total amount exchanged either from or to currency i should respect the limit
    problem += pulp.lpSum(x[i][j] for j in range(N)) + pulp.lpSum(x[j][i] for j in range(N)) <= limit[i]

# Solve the problem
problem.solve()

# Extract the results
transactions = []
for i in range(N):
    for j in range(N):
        if x[i][j].varValue > 0:
            transactions.append({
                "from": i + 1,
                "to": j + 1,
                "amount": x[i][j].varValue
            })

final_amount_of_currency_N = pulp.value(problem.objective)

# Print the result
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')