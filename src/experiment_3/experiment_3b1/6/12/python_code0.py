import pulp
import json

# Data from the provided JSON format
data = {
    'N': 3,
    'Start': [100.0, 50.0, 200.0],
    'Limit': [1000.0, 200.0, 3000.0],
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Create the problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Variables: x[i][j] for amount of currency i exchanged for currency j
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective Function: Maximize total amount of currency N
problem += pulp.lpSum(x[N-1][j] for j in range(N)), "Total_Amount_of_Currency_N"

# Constraints: Limit on exchanges for each currency
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= Limit[i], f"Limit_on_currency_{i+1}"

# Constraints: Exchange condition
for i in range(N):
    for j in range(N):
        problem += x[i][j] <= Start[i] * Rate[i][j], f"Exchange_condition_{i+1}_{j+1}"

# Solve the problem
problem.solve()

# Collect the results
transactions = []
for i in range(N):
    for j in range(N):
        if x[i][j].value() > 0:
            transactions.append({
                "from": i + 1,
                "to": j + 1,
                "amount": x[i][j].value()
            })

final_amount_of_currency_N = sum(x[N-1][j].value() for j in range(N))

# Printing the results
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')