import pulp

# Load data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Initialize the problem
problem = pulp.LpProblem("Currency_Exchange_Maximization", pulp.LpMaximize)

# Variables for the amount of currency i exchanged for currency j
exchange_amounts = pulp.LpVariable.dicts(
    "exchange",
    ((i, j) for i in range(N) for j in range(N)),
    lowBound=0
)

# Objective: maximize the final amount of currency N-1
final_currency_N_minus_1 = Start[N-1] + pulp.lpSum(exchange_amounts[i, N-1] * Rate[i][N-1] for i in range(N))
problem += final_currency_N_minus_1, "Maximize_Finality_of_Currency_N"

# Constraints
# Each currency i can be exchanged to another currency j with a limit
for i in range(N):
    problem += pulp.lpSum(exchange_amounts[i, j] for j in range(N)) <= Limit[i] + Start[i], f"Limit_Currency_{i}"

# Non-negative transactions and cannot exchange to the same currency
for i in range(N):
    for j in range(N):
        if i != j:
            problem += exchange_amounts[i, j] >= 0, f"NonNegative_{i}_{j}"

# Solve the problem
problem.solve()

# Extract results
transactions = []
for i in range(N):
    for j in range(N):
        if i != j and pulp.value(exchange_amounts[i, j]) > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": pulp.value(exchange_amounts[i, j])
            })

final_amount_of_currency_N = pulp.value(final_currency_N_minus_1)

# Output format
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

# Print the solution
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')