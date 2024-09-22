import json
import pulp

data = {'N': 3, 'Start': [100.0, 50.0, 200.0], 'Limit': [1000.0, 200.0, 3000.0], 'Rate': [[0.99, 0.9, 1.02], [0.95, 0.99, 0.92], [0.9, 0.91, 0.99]]}

N = data['N']
start = data['Start']
limit = data['Limit']
rate = data['Rate']

# Create a linear programming problem
problem = pulp.LpProblem("Currency_Exchange", pulp.LpMaximize)

# Define variables for the amount exchanged between currencies
exchange_vars = pulp.LpVariable.dicts("exchange", (range(N), range(N)), lowBound=0)

# Objective: Maximize the total amount of currency N at the end of the day
final_amount_N = pulp.LpVariable("final_amount_N", lowBound=0)
problem += final_amount_N

# Constraints for the currencies
for i in range(N):
    # Amount of currency i after transactions
    problem += (
        start[i] + pulp.lpSum(exchange_vars[i][j] for j in range(N)) -
        pulp.lpSum(exchange_vars[j][i] for j in range(N)) == 
        (final_amount_N if i == N-1 else 0),
        f"Balance_Constraint_{i}"
    )
    
    # Limit constraints
    for j in range(N):
        if i != j:
            problem += (
                exchange_vars[i][j] <= limit[i],
                f"Limit_Constraint_{i}_{j}"
            )
 
# Rate constraints
for i in range(N):
    for j in range(N):
        if i != j:
            problem += (
                exchange_vars[i][j] <= start[i] * rate[i][j],
                f"Rate_Constraint_{i}_{j}"
            )

# Solve the problem
problem.solve()

# Prepare the output
transactions = []
for i in range(N):
    for j in range(N):
        if i != j and pulp.value(exchange_vars[i][j]) > 0:
            transactions.append({
                "from": i,
                "to": j,
                "amount": pulp.value(exchange_vars[i][j])
            })

# Final amount of currency N
final_amount_of_currency_N = pulp.value(final_amount_N)

# Output dictionary
output = {
    "transactions": transactions,
    "final_amount_of_currency_N": final_amount_of_currency_N
}

# Print the final output
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')