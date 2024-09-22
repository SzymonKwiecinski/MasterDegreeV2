import pulp
import json

# Problem data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
starts = data['Start']
limits = data['Limit']
rates = data['Rate']

# Create the LP problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Decision variables
amounts = pulp.LpVariable.dicts("amount", (range(N), range(N)), lowBound=0)

# Objective function: maximize final amount of currency N
final_currency_N = pulp.lpSum(amounts[i][N-1] for i in range(N)) + starts[N-1]
problem += final_currency_N, "Total_Amount_of_Currency_N"

# Constraints: limit for each currency
for i in range(N):
    problem += pulp.lpSum(amounts[i][j] for j in range(N)) <= limits[i], f"Limit_Constraint_{i}"

# Constraints: starting amounts
for i in range(N):
    for j in range(N):
        if i != j:
            problem += amounts[i][j] <= starts[i] * rates[i][j], f"Exchange_Rate_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Prepare output
transactions = []
for i in range(N):
    for j in range(N):
        if i != j and amounts[i][j].varValue > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": amounts[i][j].varValue
            })

final_amount_of_currency_N = pulp.value(problem.objective)

# Output the result
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')