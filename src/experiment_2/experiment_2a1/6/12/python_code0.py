import pulp
import json

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the LP problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Define variables for the amount of each currency exchanged
x = pulp.LpVariable.dicts("exchange", (range(N), range(N)), lowBound=0)

# Objective function: maximize the final amount of currency N (index N-1)
problem += pulp.lpSum(x[i][N-1] * rate[i][N-1] for i in range(N)), "Total_Value"

# Constraints for starting amounts
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if i != j) <= limit[i], f"Limit_out_{i}"
    problem += pulp.lpSum(x[j][i] for j in range(N) if i != j) <= limit[i], f"Limit_in_{i}"

# Ensure we do not exceed the starting amounts for each currency
for i in range(N):
    problem += (start[i] - pulp.lpSum(x[i][j] for j in range(N) if i != j) + 
                 pulp.lpSum(x[j][i] for j in range(N) if i != j) >= 0), f"Start_amount_{i}"

# Solve the problem
problem.solve()

# Prepare the output
transactions = []
for i in range(N):
    for j in range(N):
        if i != j and x[i][j].varValue > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": x[i][j].varValue
            })

final_amount_of_currency_N = sum(start[i] - (x[i][N-1].varValue if i == N-1 else 0) + 
                                  (x[N-1][i].varValue if i != N-1 else 0) for i in range(N))

# Output the results
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')