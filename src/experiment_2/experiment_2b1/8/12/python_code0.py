import json
import pulp

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create linear programming problem
problem = pulp.LpProblem("Maximize_Currency", pulp.LpMaximize)

# Define variables for amount exchanged from currency i to currency j
exchange_vars = pulp.LpVariable.dicts("exchange", (range(N), range(N)), lowBound=0)

# Objective function: Maximize total currency N
problem += pulp.lpSum(exchange_vars[i][N-1] for i in range(N)) + start[N-1], "Total_Currency_N"

# Constraints: Limit for each currency exchange
for i in range(N):
    problem += pulp.lpSum(exchange_vars[i][j] for j in range(N)) <= limit[i], f"Limit_{i}"
    problem += pulp.lpSum(exchange_vars[j][i] for j in range(N)) <= limit[i], f"Limit_From_{i}"

# Constraints: Starting amount and exchange rates
for i in range(N):
    problem += start[i] + pulp.lpSum((rate[i][j] * exchange_vars[i][j]) for j in range(N)) - pulp.lpSum((exchange_vars[j][i]) for j in range(N)) >= 0, f"Starting_Amount_{i}"

# Solve the problem
problem.solve()

# Prepare output
transactions = []
for i in range(N):
    for j in range(N):
        if pulp.value(exchange_vars[i][j]) > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": pulp.value(exchange_vars[i][j])
            })

final_amount_of_currency_N = pulp.value(start[N-1]) + sum(pulp.value(exchange_vars[i][N-1]) for i in range(N))

# Output result
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')