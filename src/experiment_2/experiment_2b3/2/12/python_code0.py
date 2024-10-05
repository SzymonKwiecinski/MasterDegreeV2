import pulp
import json

# Load the data
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')
N = data["N"]
start = data["Start"]
limit = data["Limit"]
rate = data["Rate"]

# Initialize LP problem
problem = pulp.LpProblem("Currency_Exchange_Maximization", pulp.LpMaximize)

# Decision variables for amount of currency i to be exchanged to currency j
exchange_vars = pulp.LpVariable.dicts("Exchange", ((i, j) for i in range(N) for j in range(N)), lowBound=0)

# Objective: Maximize the units of currency N at the end of the day
problem += pulp.lpSum(exchange_vars[i, N-1] * rate[i][N-1] for i in range(N)), "Maximize_Currency_N"

# Constraints: Total amount of currency i exchanged cannot exceed the limit
for i in range(N):
    problem += (pulp.lpSum(exchange_vars[i, j] for j in range(N)) + pulp.lpSum(exchange_vars[j, i] for j in range(N))) <= limit[i], f"Limit_Currency_{i}"

# Constraints: Currency balance equations
for i in range(N):
    problem += (start[i] + pulp.lpSum(exchange_vars[j, i] * rate[j][i] for j in range(N))) - pulp.lpSum(exchange_vars[i, j] for j in range(N)) >= 0, f"Balance_Currency_{i}"

# Solve the problem
problem.solve()

# Prepare the output JSON
transactions = []
for i in range(N):
    for j in range(N):
        if pulp.value(exchange_vars[i, j]) > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": pulp.value(exchange_vars[i, j])
            })

final_amount_of_currency_N = start[N-1] + sum(pulp.value(exchange_vars[j, N-1]) * rate[j][N-1] for j in range(N))

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(json.dumps(output, indent=4))

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')