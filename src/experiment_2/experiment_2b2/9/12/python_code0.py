import pulp

# Data provided in the json format
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

# Extracting data from the JSON
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Initialize the LP problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Decision variables: amount of currency i exchanged to currency j
exchange = pulp.LpVariable.dicts("exchange", ((i, j) for i in range(N) for j in range(N)), lowBound=0)

# Objective function: maximize the final amount of currency N
# We are interested in maximizing the final amount of currency N-1 (0-indexed)
final_currency_N = (
    start[N-1] +
    pulp.lpSum(exchange[i, N-1] * rate[i][N-1] for i in range(N)) - 
    pulp.lpSum(exchange[N-1, j] for j in range(N))
)
problem += final_currency_N

# Constraints
for i in range(N):
    # Total amount of currency i exchanged in or out cannot exceed its limit
    problem += pulp.lpSum(exchange[i, j] for j in range(N)) + pulp.lpSum(exchange[j, i] for j in range(N)) <= limit[i]
    
    # Balance equation for each currency i
    problem += (
        start[i] +
        pulp.lpSum(exchange[j, i] * rate[j][i] for j in range(N)) - 
        pulp.lpSum(exchange[i, j] for j in range(N))
        == start[i]
    )

# Solve the problem
problem.solve()

# Prepare output
transactions = []
for i in range(N):
    for j in range(N):
        amount = pulp.value(exchange[i, j])
        if amount > 0:  # only record non-zero exchanges
            transactions.append({
                "from": i,
                "to": j,
                "amount": amount
            })

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": pulp.value(final_currency_N)
}

# Display results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')