import pulp

# Extract data
data = {
    'N': 3, 
    'Start': [100.0, 50.0, 200.0], 
    'Limit': [1000.0, 200.0, 3000.0], 
    'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]
}

start = data['Start']
limit = data['Limit']
rate = data['Rate']
N = data['N']

# Create a linear programming problem
problem = pulp.LpProblem("Currency_Exchange_Maximization", pulp.LpMaximize)

# Decision variables: amount of currency i exchanged to currency j
x = [[pulp.LpVariable(f"x_{i}_{j}", lowBound=0) for j in range(N)] for i in range(N)]

# Objective: Maximize the final amount of currency N
final_amount = start[N-1] + pulp.lpSum(rate[i][N-1] * x[i][N-1] for i in range(N))
problem += final_amount

# Constraints: Limit on total exchange for each currency
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) <= limit[i]

# Constraints for balance of each currency
for i in range(N):
    problem += start[i] + pulp.lpSum(rate[j][i] * x[j][i] for j in range(N)) - pulp.lpSum(x[i][j] for j in range(N)) >= 0

# Solve the problem
problem.solve()

# Prepare the output
transactions = []
for i in range(N):
    for j in range(N):
        if pulp.value(x[i][j]) > 0:
            transactions.append({'from': i+1, 'to': j+1, 'amount': pulp.value(x[i][j])})

final_amount_of_currency_N = pulp.value(final_amount)

output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')