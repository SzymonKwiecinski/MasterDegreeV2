import json
import pulp

# Input data
data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 
        'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Linear programming problem definition
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Decision variables: amount of currency exchanged from i to j
amounts = pulp.LpVariable.dicts("amount", ((i, j) for i in range(N) for j in range(N)), lowBound=0)

# Objective function: maximize the final amount of currency N
problem += pulp.lpSum(amounts[(i, N-1)] * rate[i][N-1] for i in range(N)), "MaximizeFinalCurrency"

# Constraints
for i in range(N):
    # Exchange amounts constraints
    problem += pulp.lpSum(amounts[(i, j)] for j in range(N) if j != i) <= limit[i], f"ExchangeLimit_{i}"
    problem += pulp.lpSum(amounts[(j, i)] for j in range(N) if j != i) <= limit[i], f"IncomingLimit_{i}"
    
    # Starting amount constraint
    problem += pulp.lpSum(amounts[(i, j)] for j in range(N) if j != i) + start[i] == start[i] + pulp.lpSum(amounts[(j, i)] for j in range(N) if j != i), f"Balance_{i}"

# Solve the problem
problem.solve()

# Prepare output
transactions = []
for (i, j) in amounts:
    if amounts[(i, j)].varValue > 0:
        transactions.append({"from": i, "to": j, "amount": amounts[(i, j)].varValue})

final_amount = sum(amounts[(i, N-1)].varValue * rate[i][N-1] for i in range(N))

# Output the results in the specified format
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')