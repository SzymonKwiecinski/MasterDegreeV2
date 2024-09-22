import pulp
import json

# Parse input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 
        'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the linear programming problem
problem = pulp.LpProblem("CurrencyExchange", pulp.LpMaximize)

# Decision variables for the amount exchanged from currency i to currency j
exchange_vars = pulp.LpVariable.dicts("exchange", (range(N), range(N)), lowBound=0)

# Objective function: maximize the total amount of currency N
problem += pulp.lpSum(exchange_vars[i][N-1] for i in range(N)) + start[N-1], "TotalCurrencyN"

# Constraints for starting amounts and limits
for i in range(N):
    # Amount of currency i exchanged must not exceed start[i] + limit[i]
    problem += pulp.lpSum(exchange_vars[i][j] for j in range(N) if j != i) <= start[i] + limit[i], f"LimitExchangeFrom_{i}"
    problem += pulp.lpSum(exchange_vars[j][i] for j in range(N) if j != i) <= limit[i], f"LimitExchangeTo_{i}"

# Constraints for each exchange rate
for i in range(N):
    for j in range(N):
        if i != j:
            problem += exchange_vars[i][j] <= start[i] * rate[i][j], f"RateConstraint_{i}_{j}"

# Solve the problem
problem.solve()

# Prepare transactions data
transactions = []
for i in range(N):
    for j in range(N):
        if i != j:
            amount = pulp.value(exchange_vars[i][j])
            if amount > 0:
                transactions.append({
                    "from": i,
                    "to": j,
                    "amount": amount
                })

final_amount_of_currency_N = pulp.value(start[N-1] + pulp.lpSum(exchange_vars[i][N-1] for i in range(N)))

# Prepare output
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

# Print the output
print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')