import pulp

# Extracting the data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
Start = data['Start']
Limit = data['Limit']
Rate = data['Rate']

# Define the problem
problem = pulp.LpProblem("Currency_Optimization", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), lowBound=0)

# Objective Function: Maximize total amount of currency N we have at the end of the day
problem += pulp.lpSum([x[N-1, k] for k in range(N) if k != N-1])

# Constraints

# Currency Transactions Limits
for i in range(N):
    for j in range(N):
        problem += x[i, j] <= Limit[i]

# Starting Constraints
for i in range(N):
    for j in range(N):
        problem += x[i, j] <= Start[i]

# Flow Conservation
for i in range(N):
    for j in range(N):
        if i != j:
            problem += x[i, j] - x[j, i] == 0

# Wealth Inequality Constraint
for i in range(N):
    for j in range(N):
        if Rate[i][j] <= 1:
            problem += Rate[i][j] * x[i, j] <= Start[j]

# Solve the problem
problem.solve()

# Prepare the output format
transactions = []
for i in range(N):
    for j in range(N):
        if i != j and x[i, j].varValue is not None and x[i, j].varValue > 0:
            transactions.append({'from': i, 'to': j, 'amount': x[i, j].varValue})

final_amount_of_currency_N = sum(x[N-1, j].varValue for j in range(N) if x[N-1, j].varValue is not None)

# Print the transactions and the final amount
print("Transactions:")
for transaction in transactions:
    print(transaction)

print(f'Final Amount of Currency {N}: {final_amount_of_currency_N}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')