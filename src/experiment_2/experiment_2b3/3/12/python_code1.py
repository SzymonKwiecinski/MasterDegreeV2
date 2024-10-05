import pulp
import json

# Parse the input data
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Currency_N", pulp.LpMaximize)

# Define variables for the amount to exchange from currency i to j
exchange_vars = pulp.LpVariable.dicts("Exchange", [(i, j) for i in range(N) for j in range(N)], lowBound=0, cat='Continuous')

# Objective function: maximize the final amount of currency N
problem += (start[N-1] + 
            pulp.lpSum(exchange_vars[i, N-1] * rate[i][N-1] for i in range(N) if i != N-1) -
            pulp.lpSum(exchange_vars[N-1, j] for j in range(N)), f"ObjectiveFunction")

# Constraints
for i in range(N):
    # The amount exchanged cannot exceed the limit for each currency
    problem += (pulp.lpSum(exchange_vars[i, j] for j in range(N)) + 
                pulp.lpSum(exchange_vars[j, i] * (1 / rate[j][i]) for j in range(N) if j != i) <=
                start[i] + limit[i], f"LimitConstraint_{i}")

# Solve the problem
problem.solve()

# Gather results
transactions = []
for i in range(N):
    for j in range(N):
        if pulp.value(exchange_vars[i, j]) > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": pulp.value(exchange_vars[i, j])
            })

final_amount_of_currency_N = (start[N-1] + 
                              pulp.lpSum(pulp.value(exchange_vars[i, N-1]) * rate[i][N-1] for i in range(N) if i != N-1) -
                              pulp.lpSum(pulp.value(exchange_vars[N-1, j]) for j in range(N)))

# Prepare output
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

# Print the output json
print(json.dumps(output, indent=4))

# Print the Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')