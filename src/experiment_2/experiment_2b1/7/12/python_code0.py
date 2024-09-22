import pulp
import json

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the optimization problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Define variables for the amounts exchanged
exchange_vars = pulp.LpVariable.dicts("Exchange", (range(N), range(N)), 0)

# Objective Function: Maximize the amount of final currency
final_currency = pulp.lpSum([exchange_vars[i][N-1] for i in range(N)]) + start[N-1]
problem += final_currency, "Objective"

# Constraints for each currency
for i in range(N):
    # Amount exchanged cannot exceed limits of each currency
    problem += pulp.lpSum([exchange_vars[i][j] for j in range(N)]) <= limit[i], f"Limit_Used_for_Currency_{i}"
    # Ensure that the total amount exchanged does not exceed what we start with
    problem += pulp.lpSum([exchange_vars[j][i] for j in range(N)]) <= start[i], f"Max_Exchange_for_Currency_{i}"

# Constraints for exchange rates
for i in range(N):
    for j in range(N):
        if i != j:
            problem += exchange_vars[i][j] <= start[i] * rate[i][j], f"Rate_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Prepare the transactions result
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

# Final amount of currency N
final_amount_of_currency_N = start[N-1] + pulp.value(exchange_vars[N-1][N-1])

# Output result
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')