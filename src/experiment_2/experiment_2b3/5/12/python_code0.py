import pulp
import json

# Parse the data 
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Define the problem
problem = pulp.LpProblem("Maximize_Currency_N", pulp.LpMaximize)

# Define variables
x = pulp.LpVariable.dicts("Exchange", ((i, j) for i in range(N) for j in range(N)), lowBound=0, cat='Continuous')

# Objective function: Maximize currency N
problem += pulp.lpSum([x[i, N-1] * rate[i][N-1] for i in range(N)])

# Constraints
for i in range(N):
    # The total amount of currency i exchanged cannot exceed the limit
    problem += pulp.lpSum([x[i, j] for j in range(N)]) <= limit[i], f"Limit_for_currency_{i}"
    # The total amount of currency i used cannot exceed the starting amount
    problem += pulp.lpSum([x[j, i] for j in range(N)]) <= start[i], f"Start_for_currency_{i}"

# Solve the problem
problem.solve()

# Prepare the output
transactions = []
for i in range(N):
    for j in range(N):
        if i != j:
            amount_exchanged = pulp.value(x[i, j])
            if amount_exchanged > 0:
                transactions.append({
                    "from": i,
                    "to": j,
                    "amount": amount_exchanged
                })

final_amount_of_currency_N = sum(pulp.value(x[i, N-1]) * rate[i][N-1] for i in range(N))

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

# Print the objective value
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")

# Output the result in JSON format
print(json.dumps(output, indent=2))