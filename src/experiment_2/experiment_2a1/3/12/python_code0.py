import pulp
import json

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the Linear Programming problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Variables for the amounts exchanged
exchange_vars = pulp.LpVariable.dicts("exchange", (range(N), range(N)), lowBound=0)

# Objective function: maximize the final amount of currency N
final_amount_currency_N = start[2] + pulp.lpSum([exchange_vars[i][2] for i in range(N)])
problem += final_amount_currency_N

# Constraints for limit on exchanges
for i in range(N):
    problem += pulp.lpSum([exchange_vars[i][j] for j in range(N)]) <= limit[i], f"Limit_Constraint_{i}"
    problem += pulp.lpSum([exchange_vars[j][i] for j in range(N)]) <= limit[i], f"Limit_Constraint_From_{i}"

# Constraints for starting amounts
for i in range(N):
    for j in range(N):
        if i != j:
            problem += exchange_vars[i][j] <= start[i] * rate[i][j], f"Exchange_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Prepare output
transactions = []
for i in range(N):
    for j in range(N):
        if i != j and pulp.value(exchange_vars[i][j]) > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": pulp.value(exchange_vars[i][j])
            })

final_amount = pulp.value(final_amount_currency_N)

# Output JSON format
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount
}

# Print the final output
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')