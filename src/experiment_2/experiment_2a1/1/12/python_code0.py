import pulp
import json

data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
starts = data['Start']
limits = data['Limit']
rates = data['Rate']

# Create the LP problem
problem = pulp.LpProblem("CurrencyExchange", pulp.LpMaximize)

# Define variables for the amounts exchanged between currencies
amounts = pulp.LpVariable.dicts("Amount", (range(N), range(N)), 0)

# Objective Function: Maximize final units of currency N
final_amount_N = starts[2] + pulp.lpSum(amounts[i][2] * rates[i][2] for i in range(N))
problem += final_amount_N

# Constraints for starting currency amounts and limits
for i in range(N):
    problem += pulp.lpSum(amounts[i][j] for j in range(N)) <= limits[i]
    problem += amounts[i][i] == 0  # cannot exchange same currency

# Constraints for starting amounts
for j in range(N):
    problem += starts[j] + pulp.lpSum(amounts[i][j] * rates[i][j] for i in range(N)) - pulp.lpSum(amounts[j][i] for i in range(N)) >= 0

# Solve the problem
problem.solve()

# Prepare the output
transactions = []
for i in range(N):
    for j in range(N):
        if amounts[i][j].varValue > 0:
            transactions.append({"from": i, "to": j, "amount": amounts[i][j].varValue})

final_amount_currency_N = pulp.value(final_amount_N)

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_currency_N
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')