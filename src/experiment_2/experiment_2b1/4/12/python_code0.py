import pulp
import json

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the LP problem
problem = pulp.LpProblem("Currency_Exchange_Problem", pulp.LpMaximize)

# Variables for amount exchanged from currency i to currency j
amounts = pulp.LpVariable.dicts("amount", (range(N), range(N)), lowBound=0, cat='Continuous')

# Objective Function: Maximize final amount of currency N
problem += pulp.lpSum(amounts[i][N-1] * rate[i][N-1] for i in range(N)), "Total_Amount_of_Currency_N"

# Constraints for starting amounts
for i in range(N):
    problem += pulp.lpSum(amounts[j][i] for j in range(N)) - pulp.lpSum(amounts[i][j] for j in range(N)) <= start[i], f"Starting_Amount_Constraint_{i}"

# Limits on currency exchanges
for i in range(N):
    problem += pulp.lpSum(amounts[i][j] for j in range(N)) <= limit[i], f"Limit_Constraint_{i}"

# Solve the problem
problem.solve()

# Collecting transactions
transactions = []
for i in range(N):
    for j in range(N):
        if amounts[i][j].varValue > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": amounts[i][j].varValue
            })

# Final amount of currency N
final_amount_currency_N = sum(amounts[i][N-1].varValue * rate[i][N-1] for i in range(N))

# Output result
result = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_currency_N
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')