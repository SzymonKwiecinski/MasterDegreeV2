import pulp
import json

# Input Data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the LP problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Variables for the amount of currency exchanged from i to j
x = pulp.LpVariable.dicts("x", (range(N), range(N)), lowBound=0)

# Objective: Maximize final amount of currency N (index N-1)
final_currency_N = start[2] + pulp.lpSum(x[i][2] * rate[i][2] for i in range(N)) - pulp.lpSum(x[2][j] for j in range(N))
problem += final_currency_N

# Constraints for limits
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= limit[i]
    problem += pulp.lpSum(x[j][i] for j in range(N)) <= limit[i]

# Constraints for initial amounts
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= start[i]

# Solve the problem
problem.solve()

# Prepare output
transactions = []
for i in range(N):
    for j in range(N):
        if x[i][j].varValue > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": x[i][j].varValue
            })

final_amount_of_currency_N = pulp.value(final_currency_N)

# Output Format
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

# Convert output to JSON format
output_json = json.dumps(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')