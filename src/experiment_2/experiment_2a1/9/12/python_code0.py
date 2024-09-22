import pulp
import json

# Input data
data = {'N': 3, 
        'Start': [100.0, 50.0, 200.0], 
        'Limit': [1000.0, 200.0, 3000.0], 
        'Rate': [[0.99, 0.9, 1.02], 
                 [0.95, 0.99, 0.92], 
                 [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create the LP problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Define variables
amounts = pulp.LpVariable.dicts("amount", ((i, j) for i in range(N) for j in range(N) if i != j), lowBound=0)

# Objective function: maximize final amount of currency N
final_currency_N = start[2] + pulp.lpSum(amounts[(i, 2)] * rate[i][2] for i in range(N) if i != 2)
problem += final_currency_N

# Constraints
for i in range(N):
    problem += pulp.lpSum(amounts[(i, j)] for j in range(N) if i != j) <= limit[i]
    problem += pulp.lpSum(amounts[(j, i)] for j in range(N) if i != j) <= limit[i]

# Starting amounts constraints
for i in range(N):
    problem += start[i] - pulp.lpSum(amounts[(j, i)] for j in range(N) if i != j) + \
               pulp.lpSum(amounts[(i, j)] for j in range(N) if i != j) >= 0

# Solve the problem
problem.solve()

# Gather results
transactions = []
for (i, j), variable in amounts.items():
    if variable.varValue > 0:
        transactions.append({
            "from": i,
            "to": j,
            "amount": variable.varValue
        })

# Final amount of currency N
final_amount_of_currency_N = start[2] + sum(amounts[(i, 2)].varValue * rate[i][2] for i in range(N) if i != 2)

# Prepare output
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')