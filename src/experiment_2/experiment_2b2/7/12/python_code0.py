import pulp
import json

# Parse the input JSON data
data = json.loads('{"N": 3, "Start": [100.0, 50.0, 200.0], "Limit": [1000.0, 200.0, 3000.0], "Rate": [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}')

# Unpack the data
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Initialize the LP problem
problem = pulp.LpProblem("CurrencyExchange", pulp.LpMaximize)

# Create the variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0)

# Objective: Maximize the final amount of currency N
problem += pulp.lpSum(x[i][N-1] * rate[i][N-1] for i in range(N-1))

# Constraints
for i in range(N):
    # Limit on currency exchange
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= limit[i]
    # Conservation of currency flow
    problem += start[i] + pulp.lpSum(x[j][i] * rate[j][i] for j in range(N)) - pulp.lpSum(x[i][j] for j in range(N)) >= 0

# Solve the problem
problem.solve()

# Prepare the output
transactions = []
for i in range(N):
    for j in range(N):
        if pulp.value(x[i][j]) > 0:
            transactions.append({"from": i, "to": j, "amount": pulp.value(x[i][j])})

final_amount_of_currency_N = start[N-1] + pulp.lpSum(pulp.value(x[i][N-1]) * rate[i][N-1] for i in range(N-1))

# Output JSON
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')