import pulp
import json

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the LP problem
problem = pulp.LpProblem("CurrencyExchange", pulp.LpMaximize)

# Define the variables for the amounts to exchange from currency i to j
amounts = pulp.LpVariable.dicts("Amount", (range(N), range(N)), lowBound=0)

# Objective function: maximize the total amount of currency 3 (index 2)
problem += pulp.lpSum(amounts[i][2] for i in range(N)), "TotalCurrencyN"

# Constraints
for i in range(N):
    problem += pulp.lpSum(amounts[i][j] for j in range(N)) <= limit[i], f"Limit_{i}"  # Total exchange from currency i
    problem += pulp.lpSum(amounts[j][i] for j in range(N)) <= limit[i], f"LimitIncoming_{i}"  # Total exchange to currency i

# Start amounts constraints
for i in range(N):
    problem += pulp.lpSum(amounts[i][j] for j in range(N)) - pulp.lpSum(amounts[j][i] for j in range(N)) + start[i] >= 0, f"StartAmount_{i}"

# Solve the problem
problem.solve()

# Prepare the output
transactions = []
for i in range(N):
    for j in range(N):
        if amounts[i][j].varValue > 0:
            transactions.append({
                'from': i,
                'to': j,
                'amount': amounts[i][j].varValue
            })

final_amount = sum(amounts[i][2].varValue for i in range(N)) + start[2]

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')