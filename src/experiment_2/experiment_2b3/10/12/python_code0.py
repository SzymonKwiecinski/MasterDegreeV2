import pulp

# Load data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

# Extract data
N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Define the problem
problem = pulp.LpProblem("Maximize_Final_Currency", pulp.LpMaximize)

# Define variables for the amount of currency i exchanged to currency j
x = pulp.LpVariable.dicts("x", [(i, j) for i in range(N) for j in range(N)], lowBound=0, cat='Continuous')

# Objective function: Maximize the amount of currency N we end up with
problem += pulp.lpSum(x[i, N-1] * rate[i][N-1] for i in range(N))

# Constraints
# Total amount constraint for each currency
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= start[i] + pulp.lpSum(x[j, i] * rate[j][i] for j in range(N))
    problem += pulp.lpSum(x[i, j] for j in range(N)) <= limit[i]

# Solve the problem
problem.solve()

# Extract transactions and final currency N amount
transactions = []
for i in range(N):
    for j in range(N):
        amount = pulp.value(x[i, j])
        if amount > 0:
            transactions.append({"from": i, "to": j, "amount": amount})

final_amount_of_currency_N = pulp.value(pulp.lpSum(x[i, N-1] * rate[i][N-1] for i in range(N)))

# Output result
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')